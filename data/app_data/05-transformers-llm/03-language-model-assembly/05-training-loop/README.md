---
name: txf-lm-training-loop
title: 'Training loop for next-token prediction (reuses Part 1 loop)'
tags: [transformers, nlp]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[03-dl-training/03-training-loop/02-assemble-training-loop]` established the pattern every training loop in this curriculum follows: forward pass, compute loss and its gradient, backward pass, update the weights, repeat, demonstrated there for one linear layer trained with MSE. This question applies the EXACT SAME pattern to `[04-full-forward-pass]`'s language model, with one deliberate, explicitly-scoped simplification: it trains `[01-output-projection]`'s output head via REAL backpropagation (reusing `[03-dl-training/02-layers/02-linear-backward]`'s `linear_backward` directly, since the output projection IS an ordinary linear layer), while treating the Transformer blocks' output (`hidden_states`) as FIXED, given input features, exactly the same "linear probe on frozen features" setup widely used in practice when fine-tuning only a model's final layer.

This scoping is a genuine, honest choice, not a shortcut: full end-to-end backpropagation through `[01-transformer-block]`'s attention and feed-forward sublayers is real, well-defined math, but implementing it requires a backward pass for every piece in that stack, work this curriculum's Transformer-block questions deliberately left as FORWARD-only (mirroring how they were actually built and tested throughout this Part). What this question DOES demonstrate, completely and correctly, is the entire remaining training-loop machinery, loss computation, gradient computation, and a genuine weight update that provably reduces the loss, applied to language modeling specifically.

### From theory to code

Implement `train_output_head_one_step(hidden_states, token_ids, output_weight, lr)`: `[01-output-projection]`'s forward pass, `[03-next-token-cross-entropy]`'s loss (via the lower-level `cross_entropy_forward`/`cross_entropy_backward`), `[02-layers/02-linear-backward]`'s backward pass, and an SGD update, and `train_output_head(hidden_states, token_ids, output_weight, lr, num_steps)`, looping that single step `num_steps` times.

### Constraints

- `hidden_states` and `token_ids` are shifted by one position first, exactly `[03-next-token-cross-entropy]`'s pattern: the LAST position's hidden state has no next-token target and must be excluded before computing the loss/gradient.
- The gradient with respect to `output_weight` comes from `[02-layers/02-linear-backward]`'s `linear_backward`, called with the (shifted, flattened) hidden states as its `x` argument, exactly like `[02-layers/02-linear-backward]`'s own linear-layer backward pass.
- The weight update is `output_weight - lr * grad_output_weight`, ordinary SGD, exactly `[03-dl-training/03-training-loop/02-assemble-training-loop]`'s update rule.
- `train_output_head_one_step` returns the loss computed BEFORE the update (what the weight actually achieved going into this step), not after.

### Hints

<details>
<summary>Hint 1: Shifting and flattening (exactly [03-next-token-cross-entropy]'s pattern)</summary>

```python
predicted_hidden = hidden_states[..., :-1, :]
targets = token_ids[..., 1:]
flat_hidden = predicted_hidden.reshape(-1, d_model)
flat_targets = targets.reshape(-1)
```

</details>

<details>
<summary>Hint 2: Forward, loss, and gradient</summary>

```python
logits = output_projection(flat_hidden, output_weight)
loss = cross_entropy_forward(logits, flat_targets)
grad_logits = cross_entropy_backward(logits, flat_targets)
```

</details>

<details>
<summary>Hint 3: Backward and the update</summary>

`_, grad_output_weight, _ = linear_backward(grad_logits, flat_hidden, output_weight)` (the output projection has no bias, so the bias gradient is simply discarded), then `updated_output_weight = output_weight - lr * grad_output_weight`.

</details>

## Theory

### The simple version

`[03-dl-training/03-training-loop/02-assemble-training-loop]`'s student adjusting one dial (their linear model's weight) based on how wrong their predictions were, over and over, each adjustment nudging the dial in whichever direction actually reduces the error. This question is the exact same student, the exact same procedure, just now grading NEXT-WORD predictions instead of a numeric regression target, and adjusting only the FINAL dial in a longer chain of dials (the output head), treating everything upstream of it as already fixed for this particular training step.

### The formula

```
predicted_hidden, targets = shift(hidden_states, token_ids)   # like 03-next-token-cross-entropy
logits = predicted_hidden @ output_weight^T
loss = CrossEntropy(logits, targets)
grad_logits = CrossEntropy_backward(logits, targets)
grad_output_weight = grad_logits^T @ predicted_hidden           # linear_backward's formula
output_weight = output_weight - lr * grad_output_weight
```

### How PyTorch actually implements this

`loss.backward()` followed by `optimizer.step()` performs exactly this sequence for an ENTIRE model at once (every layer, not just the output head), since PyTorch's `autograd` automatically computes gradients through arbitrarily deep computation graphs, a capability this curriculum's `[02-deep-learning-core/04-autograd]` section built a small version of from scratch. This question's explicit "hidden_states as fixed input, output head trained via real backprop" scope is genuinely how "linear probing" works in practice (a common, cheap way to adapt a large pretrained model's LAST layer to a new task without touching, or paying the compute cost of updating, everything beneath it), not merely a simplification invented for this curriculum.

## Explanation

`train_output_head_one_step` shifts `hidden_states` and `token_ids` by one position (`[03-next-token-cross-entropy]`'s exact pattern), computes logits via `[01-output-projection]`'s forward pass, and calls `cross_entropy_forward`/`cross_entropy_backward` to get both the loss VALUE and the gradient of that loss with respect to the logits. `linear_backward(grad_logits, flat_hidden, output_weight)` (reused directly from `[03-dl-training/02-layers/02-linear-backward]`, since the output projection is exactly that kind of linear layer) then computes `grad_output_weight = grad_logits.T @ flat_hidden`, the gradient telling the update EXACTLY which direction to move `output_weight` to reduce this batch's loss. Subtracting `lr * grad_output_weight` from `output_weight` is ordinary SGD, the identical update rule `[03-dl-training/03-training-loop/02-assemble-training-loop]` already used. `train_output_head` simply repeats this one step `num_steps` times, and the resulting loss history reliably decreases on a fixed batch, exactly the behavior a correct gradient-descent implementation should produce.
