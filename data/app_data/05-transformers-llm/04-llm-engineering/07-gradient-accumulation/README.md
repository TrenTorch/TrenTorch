---
name: txf-llmeng-gradient-accumulation
title: 'Gradient accumulation: simulating a larger batch size than memory allows'
tags: [transformers, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[03-language-model-assembly/05-training-loop]`'s `train_output_head_one_step` computes a gradient from ONE batch and immediately applies it. Larger batches generally give a more stable, less noisy gradient estimate, but a batch's memory footprint grows with its size, and eventually a desired batch size simply doesn't fit in available memory all at once, a real, common constraint when training large models. Gradient accumulation resolves this without needing more memory: split the desired large batch into several smaller MICRO-batches that DO fit individually, compute each micro-batch's gradient SEPARATELY (never holding more than one micro-batch in memory at a time), average those gradients together, and apply only ONE weight update using the averaged result, mathematically equivalent to having computed the gradient on the full large batch directly.

The correctness of this trick rests on one precise mathematical fact: for a MEAN-reduced loss (`[03-next-token-cross-entropy]`'s default), the gradient of the mean over a large batch equals the MEAN of the gradients of the mean over equal-sized smaller groups that partition it (a nested average of equal-sized groups is exactly the overall average). Get the averaging wrong (accumulate via SUM instead of MEAN, say) and the effective step size silently changes with the number of micro-batches, a subtle, easy-to-introduce training bug.

### From theory to code

Implement `compute_output_head_gradient(hidden_states, token_ids, output_weight)` (`[05-training-loop]`'s gradient computation, without the update), `accumulate_gradients(gradients)` (the elementwise mean across micro-batch gradients), and `train_with_gradient_accumulation(micro_batches, output_weight, lr)`, combining them into one full accumulation-then-update cycle.

### Constraints

- Every micro-batch's gradient is computed INDEPENDENTLY, with `output_weight` held FIXED across all of them (no intermediate updates between micro-batches).
- `accumulate_gradients` averages (MEAN), never sums, the micro-batch gradients.
- Exactly ONE weight update happens, using the accumulated (averaged) gradient, after ALL micro-batches have been processed.
- For equal-sized micro-batches, the resulting update must be IDENTICAL (up to floating-point precision) to computing the gradient directly on the full concatenated batch in one shot.

### Hints

<details>
<summary>Hint 1: Per-micro-batch gradients</summary>

`compute_output_head_gradient` is exactly `[05-training-loop]`'s `train_output_head_one_step`, with the final `output_weight - lr * grad_output_weight` line removed, returning `(grad_output_weight, loss)` directly instead.

</details>

<details>
<summary>Hint 2: Accumulating and updating</summary>

```python
gradients = [compute_output_head_gradient(h, t, output_weight)[0] for h, t in micro_batches]
accumulated_grad = np.mean(gradients, axis=0)
updated_weight = output_weight - lr * accumulated_grad
```

</details>

## Theory

### The simple version

A student who wants to estimate a large population's average height, but can only survey small groups at a time (limited resources). Surveying several equal-sized small groups SEPARATELY, averaging each group's own average, then averaging THOSE group averages together, gives EXACTLY the same answer as if they'd somehow surveyed the entire population at once (as long as every group is the same size), a basic property of averaging nested groups. Gradient accumulation applies the identical logic to gradients: several small "surveys" (micro-batch gradients), combined by averaging, stand in mathematically for one large survey (the full-batch gradient) that memory constraints simply won't allow directly.

### The formula

```
grad_1 = gradient(micro_batch_1, weight)
grad_2 = gradient(micro_batch_2, weight)
  ...
grad_N = gradient(micro_batch_N, weight)

accumulated_grad = mean(grad_1, ..., grad_N)
weight = weight - lr * accumulated_grad
```

Mathematically equivalent to `gradient(concat(micro_batch_1, ..., micro_batch_N), weight)`, PROVIDED every micro-batch has the same number of examples (unequal-sized micro-batches need a WEIGHTED average instead, by each micro-batch's own example count, outside this question's scope).

### How PyTorch actually implements this

```python
for micro_batch in micro_batches:
    loss = compute_loss(micro_batch) / len(micro_batches)
    loss.backward()   # accumulates INTO .grad, since PyTorch's autograd adds rather than overwrites by default
optimizer.step()
optimizer.zero_grad()
```

is the standard PyTorch pattern: dividing each micro-batch's loss by the total micro-batch COUNT before calling `.backward()` achieves the same averaging effect this question's explicit `np.mean` does, relying on `autograd`'s default behavior of ADDING new gradients onto whatever `.grad` already holds (rather than replacing it), across repeated `.backward()` calls, until `optimizer.step()` finally applies the accumulated result and `optimizer.zero_grad()` resets for the next accumulation cycle. `[08-resume-from-checkpoint]`, immediately following this question, examines a related but distinct concern: correctly SAVING and RESTORING an optimizer's own internal state (not gradients, but persistent per-parameter statistics like Adam's moving averages) across a training interruption.

## Explanation

`compute_output_head_gradient` factors `[05-training-loop]`'s gradient computation out from its weight-update step, returning the raw `(grad_output_weight, loss)` pair for a single micro-batch, leaving `output_weight` itself untouched. `accumulate_gradients` computes `np.mean(gradients, axis=0)`, the elementwise average across however many micro-batch gradients were collected. `train_with_gradient_accumulation` loops over every micro-batch, computing (but never applying) each one's own gradient against the SAME starting `output_weight`, accumulates them via the mean, and applies exactly one `output_weight - lr * accumulated_grad` update at the very end. Because averaging is linear, and every micro-batch in the test cases has the same number of examples, this two-stage "average of per-micro-batch means" produces EXACTLY the same numeric gradient (and therefore the same weight update) as computing the gradient directly on the full concatenated batch in one pass, the property that makes gradient accumulation a genuine, exact simulation of a larger batch size rather than merely an approximation of one.
