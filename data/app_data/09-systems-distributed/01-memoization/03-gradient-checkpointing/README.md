---
name: systems-distributed-gradient-checkpointing
title: 'Gradient Checkpointing: Recompute Activations in Backward Instead of Storing Them'
tags: [mlops, neural-networks, memoization]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`01-kv-cache-autoregressive-generation` cached results _forward_ in time (reuse past K/V instead of recomputing them) to save compute at the cost of memory. Gradient checkpointing makes the exact opposite trade, on the training side of the same network: a standard backward pass needs every layer's intermediate activation kept in memory (there are `num_layers + 1` of them, all alive at once), which becomes the actual memory bottleneck for very deep networks — gradient checkpointing throws those intermediates away after the forward pass and _recomputes_ them, on demand, during backward, trading extra compute for far less peak memory.

### From theory to code

Implement `linear_backward`, `forward_full`/`backward_full` (the standard, memory-heavy approach), `forward_checkpointed`/`backward_checkpointed` (which keeps nothing but the original input, recomputing everything else when backward needs it), and `count_stored_activations`, quantifying the memory difference.

### Constraints

- `forward_full` returns `(final_output, activations, pre_activations)`, storing every intermediate value.
- `forward_checkpointed` returns only `final_output` — nothing else is kept.
- `backward_checkpointed` must produce results numerically identical to `backward_full` on the same computation — checkpointing changes _when_ things are computed, never _what_ the answer is.
- `count_stored_activations(num_layers, use_checkpointing)` returns `num_layers + 1` without checkpointing, `1` with it.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`linear_backward` is the same chain-rule reasoning `03-mse-gradient`'s Theory already built up, applied to a general `Linear` layer instead of directly to a loss: `grad_input = grad_output @ weight`, `grad_weight = grad_output.T @ input`, `grad_bias = grad_output.sum(axis=0)`.

</details>

<details>
<summary>Hint 2</summary>

`backward_checkpointed` doesn't need any new backward-pass logic at all — it just calls `forward_full` first (to regenerate the activations that were never stored), then hands the result straight to `backward_full`, unmodified.

</details>

## Theory

### The simple version

Imagine taking detailed notes on every single page of a long book as you read it, so you can answer questions about any earlier page instantly later — versus taking no notes at all, and simply re-reading from the last bookmark whenever a question about an earlier page comes up. The first approach uses a lot of paper (memory) but answers instantly; the second uses almost no paper but has to spend extra time re-reading when a question actually arrives. Gradient checkpointing is exactly the second approach, applied to a neural network's forward-pass activations: don't keep detailed notes on every layer, just remember where you started, and re-derive whatever's needed, exactly when it's needed.

### The formula

```text
forward_full(x):        keeps [x, layer1_out, layer2_out, ..., layerN_out]  -- N+1 stored arrays
forward_checkpointed(x): keeps only the running `current` value, discards everything after computing it

backward_checkpointed(grad_output, x, ...):
    activations, pre_activations = forward_full(x, ...)   # RECOMPUTE, since nothing was kept
    return backward_full(grad_output, activations, pre_activations, ...)  # then backprop normally
```

The memory saved is real and substantial (`num_layers + 1` stored activations down to just `1`), and it comes at the cost of running the forward pass _twice_ per training step instead of once — a real, deliberate compute-for-memory trade, not a free optimization the way `01-kv-cache-autoregressive-generation`'s KV-cache is (which saves both compute _and_ is memory-neutral, since it stores something that would otherwise need recomputing anyway).

### How PyTorch actually implements this

Context only, untested by your submission: `torch.utils.checkpoint.checkpoint(function, *inputs)` implements exactly this — it runs `function` in a special mode during the forward pass that discards intermediate activations rather than saving them for backward, and re-runs `function` a second time during the backward pass specifically to regenerate what's needed. It's a standard technique for training very deep networks (or very long sequences through a transformer) that would otherwise run out of GPU memory purely from holding every layer's activations simultaneously — often applied selectively, checkpointing only some layers, to balance the memory savings against the extra recomputation cost.

## Explanation

`linear_backward` implements the standard Linear-layer gradient formulas directly: `grad_input` propagates the upstream gradient back through the weight matrix, `grad_weight` is the outer product of the upstream gradient and this layer's own input, and `grad_bias` sums the upstream gradient across the batch.

`forward_full` builds up `activations` (starting with `x` itself) and `pre_activations` (the pre-ReLU `Linear` output at each layer) as it runs forward, giving `backward_full` everything it needs to walk the layers in reverse, applying `relu_backward` then `linear_backward` at each one and collecting `grad_weight`/`grad_bias` for every layer along the way.

`forward_checkpointed` runs the identical computation but reassigns `current` in place each iteration, building no lists at all — by the time it returns, every intermediate value is already gone. `backward_checkpointed` compensates by calling `forward_full` on the original `x` (the one thing checkpointing _did_ keep) to regenerate exactly the `activations`/`pre_activations` `backward_full` needs, then delegates to `backward_full` unchanged — which is exactly why its output is guaranteed to match `backward_full`'s bit-for-bit: it's the same function, called on freshly-recomputed (but numerically identical) intermediate values.
