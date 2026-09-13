---
name: rl-alignment-lora-low-rank-adapters
title: "LoRA: Low-Rank Adapter Matrices Bolted Onto Part 1's Linear Layer"
tags: [reinforcement-learning, neural-networks]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`rl-alignment-qlora-quantized-lora` used LoRA's forward pass as one ingredient in a bigger quantization story. This question builds LoRA itself, in full, from scratch: a way to fine-tune a huge frozen `Linear` layer (`linear-regression-hypothesis-function`'s function, unchanged) by training only a tiny low-rank ADDITION to its output — including deriving the backward pass, which QLoRA's exercise didn't need.

### From theory to code

Implement `lora_forward` (base output plus a scaled low-rank delta) and `lora_backward` (gradients for ONLY the trainable LoRA matrices — the base layer stays completely frozen).

### Constraints

- `lora_forward(input, base_weight, base_bias, lora_A, lora_B, alpha, rank)` returns `(output, cache)`, where `output = linear(input, base_weight, base_bias) + (alpha/rank) * (input @ lora_A.T) @ lora_B.T`.
- `lora_A` has shape `(rank, in_features)`; `lora_B` has shape `(out_features, rank)`.
- `lora_backward(grad_output, cache, lora_B, alpha, rank)` returns `(grad_A, grad_B)` ONLY — never `grad_weight`/`grad_bias`, since the base layer is frozen.
- Setting `lora_A`/`lora_B` to all zeros must make `lora_forward` reduce exactly to the plain frozen `linear` call.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Think of the LoRA path as two chained `Linear`-like operations with no bias: `intermediate = input @ lora_A.T` (projecting down to `rank` dimensions), then `delta = scale * (intermediate @ lora_B.T)` (projecting back up to `out_features`) — backprop through it exactly the way you'd backprop through two stacked linear layers.

</details>

<details>
<summary>Hint 2</summary>

`grad_B` follows the same `grad_weight = grad_output.T @ input` pattern `03-gradient-checkpointing`'s `linear_backward` used, applied to the `intermediate -> delta` step; `grad_A` follows the same pattern applied to the `input -> intermediate` step, using the gradient THROUGH `lora_B` (`grad_output @ lora_B`) as its own "grad_output".

</details>

## Theory

### The simple version

Imagine a massive, expensive-to-modify machine (the frozen base weight) that you're not allowed to rebuild, but you're allowed to bolt a small, cheap "correction gearbox" onto its output shaft — this gearbox first compresses the input down to a much smaller number of dimensions (`lora_A`), then expands it back up (`lora_B`), and its whole output just gets ADDED to the big machine's normal output. Training only ever touches the small gearbox's gears, never the big machine itself, which is exactly why this is so much cheaper than retraining the whole machine.

### The formula

```text
lora_forward(x, W, b, A, B, alpha, r):
    intermediate = x @ A.T                          -- (batch, r), the "compression" step
    delta = (alpha/r) * (intermediate @ B.T)          -- (batch, out_features), the "expansion" step
    output = linear(x, W, b) + delta                 -- frozen base output + trainable delta

lora_backward(grad_output, cache, B, alpha, r):
    grad_B = (alpha/r) * grad_output.T @ intermediate
    grad_intermediate = (alpha/r) * grad_output @ B
    grad_A = grad_intermediate.T @ x
    -- NO grad_weight, NO grad_bias: the base layer is frozen
```

The `alpha/rank` scaling factor is a real, standard LoRA hyperparameter convention: it lets `alpha` control the delta's overall magnitude somewhat independently of how `rank` is chosen, so switching to a different rank doesn't automatically require re-tuning every other hyperparameter in the training recipe.

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact adapter structure from "LoRA: Low-Rank Adaptation of Large Language Models" (Hu et al., 2021) — real implementations (Hugging Face's `peft` library) wrap an existing `nn.Linear` module, freeze its original `weight`/`bias` (`requires_grad=False`), and register `lora_A`/`lora_B` as new trainable parameters whose product gets added to the frozen layer's output during the forward pass, exactly matching this exercise's structure.

## Explanation

`lora_forward` computes the low-rank delta as two chained matrix multiplications and adds it to the ordinary (frozen) `linear` output — this exercise's `tests.py` confirms that zeroing both LoRA matrices exactly recovers the frozen base layer's output, and that `alpha` scales the delta's contribution linearly, independent of the base output.

`lora_backward` treats the delta path as its own small two-layer computation and backprops through it using the same chain-rule pattern `03-gradient-checkpointing`'s `linear_backward` established, but critically returns gradients for ONLY `lora_A`/`lora_B` — `tests.py` verifies both gradients match a finite-difference numerical check (not just internal self-consistency), and confirms that perturbing the FROZEN base weight arbitrarily has zero effect on the computed LoRA gradients, directly ruling out a mutant that accidentally lets gradient information leak through the supposedly-frozen base layer.
