---
name: dl-training-assemble-training-loop
title: 'Assemble full loop (data, forward, loss, backward, optimizer step)'
tags: [neural-networks, training]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every piece this question needs already exists somewhere earlier in this curriculum: `[03-training-loop/01-dataset-dataloader]`'s `DataLoader` produces batches, `[02-layers/01-linear-forward]`'s `linear_forward` and `[02-layers/02-linear-backward]`'s `linear_backward` handle the model's forward and backward pass, and `[03-dl-training/01-optimizers]`'s `sgd_step` (or any of the other optimizer questions) handles the parameter update. What's been MISSING is the glue that wires all of them together into the actual loop every training script runs: pull a batch, run it forward, measure how wrong the prediction was, backpropagate that error, nudge the parameters a little in the direction that reduces it, and repeat for every batch in the dataset.

This is, in a very real sense, the entire "training a model" story in miniature: everything more sophisticated later in this curriculum, deeper networks, attention, transformers, is still fundamentally this same five-step loop, just with a more elaborate forward pass and a more elaborate model to differentiate through.

### From theory to code

Implement `mse_loss_and_grad(pred, target)`, which returns `(loss, grad_pred)` together in one call (mean squared error, and its gradient with respect to `pred`), and `train_one_epoch(loader, weight, bias, lr)`, which loops over every batch `DataLoader` yields, and for each one: runs `linear_forward` to get a prediction, calls `mse_loss_and_grad` to get the loss and its gradient, calls `linear_backward` to backpropagate that gradient into `grad_weight` and `grad_bias`, and updates `weight`/`bias` with a plain SGD step (`param - lr * grad`). Track the running total loss across batches and return the average, along with the updated `weight` and `bias`.

### Constraints

- `mse_loss_and_grad` computes MSE as the mean of squared errors over ALL entries (not just the batch dimension, if `pred` has multiple output features, average over those too).
- `train_one_epoch` must update `weight` and `bias` immediately after each batch (not accumulate gradients across the whole epoch and update once at the end); this is standard mini-batch SGD, not full-batch gradient descent.
- The returned average loss is the mean of each batch's OWN average loss across all batches in the epoch, not weighted differently by batch size.
- Reuse `linear_forward` and `linear_backward`, don't reimplement the matrix operations here.

### Hints

<details>
<summary>Hint 1: mse_loss_and_grad</summary>

`loss = mean((pred - target)^2)`. For the gradient: since `loss` is the mean over `pred.size` total entries of `(pred_i - target_i)^2`, and `d/dp[(p-t)^2] = 2(p-t)`, the gradient of the MEAN is `2*(pred - target) / pred.size` (dividing by the total element count, not just the batch size, to match the mean in the loss).

</details>

<details>
<summary>Hint 2: One epoch, one batch at a time</summary>

`for batch_x, batch_y in loader:` gives you one batch per iteration. Inside the loop: `pred = linear_forward(batch_x, weight, bias)`, then `loss, grad_pred = mse_loss_and_grad(pred, batch_y)`, then `_, grad_weight, grad_bias = linear_backward(grad_pred, batch_x, weight)`.

</details>

<details>
<summary>Hint 3: Updating and tracking</summary>

`weight = weight - lr * grad_weight` and `bias = bias - lr * grad_bias`, applied INSIDE the loop, right after computing the gradients for that batch (not saved up for later). Accumulate `total_loss += loss` and a batch counter, then return `total_loss / n_batches` after the loop ends.

</details>

## Theory

### The simple version

Learning to shoot free throws: you take a shot (forward pass), see how far off the rim you were (loss), figure out which direction and how much to adjust your form based on that specific miss (backward pass), make a small adjustment (optimizer step), and take the NEXT shot with your improved form. Repeat that one cycle enough times, across enough shots (batches), and your form (the model's parameters) gradually converges toward something that reliably scores. Full-batch gradient descent, taking one shot analyzing ALL your past misses at once before adjusting, would work in principle, but is far slower to get useful feedback from than adjusting after every single shot (mini-batch SGD).

### The formula

For MSE with `n` total elements in `pred`:

```
loss = (1/n) * sum((pred_i - target_i)^2)
grad_pred = (2/n) * (pred - target)
```

One epoch:

```
for each batch (batch_x, batch_y) in loader:
    pred = linear_forward(batch_x, weight, bias)
    loss, grad_pred = mse_loss_and_grad(pred, batch_y)
    grad_x, grad_weight, grad_bias = linear_backward(grad_pred, batch_x, weight)
    weight = weight - lr * grad_weight
    bias = bias - lr * grad_bias
```

### How PyTorch actually implements this

A real PyTorch training loop is this exact same five-step shape, spelled out explicitly rather than hidden behind a single function call:

```python
for batch_x, batch_y in loader:
    optimizer.zero_grad()
    pred = model(batch_x)
    loss = loss_fn(pred, batch_y)
    loss.backward()
    optimizer.step()
```

`optimizer.zero_grad()` exists because PyTorch's `.grad` attributes ACCUMULATE by default (`+=`, not `=`) across multiple `.backward()` calls, a deliberate design choice that supports gradient accumulation for effectively larger batch sizes on limited GPU memory, but means a training loop that forgets `zero_grad()` will silently sum gradients across every batch instead of computing each batch's own gradient. `loss.backward()` walks the SAME kind of computation graph `[02-deep-learning-core/04-autograd]`'s `Value` class builds by hand, and `optimizer.step()` is exactly what this question's manual `weight = weight - lr * grad_weight` line does, generalized to work over an arbitrary list of parameters and any optimizer's own update rule (`sgd_step`, `adam_step`, and so on, all from `[03-dl-training/01-optimizers]`).

## Explanation

`mse_loss_and_grad` computes `loss = mean((pred - target)^2)` directly, and `grad_pred = 2.0 * (pred - target) / pred.size`: dividing by `pred.size` (the total element count across every entry, not just the batch dimension) matches the `mean` used in the loss itself, so the gradient is consistent with exactly what `loss` measures.

`train_one_epoch` loops over every batch the `loader` yields, and for each one: computes `pred` via `linear_forward`, gets `loss` and `grad_pred` via `mse_loss_and_grad`, backpropagates via `linear_backward` to get `grad_weight` and `grad_bias`, and immediately applies a plain SGD update to `weight` and `bias`, before moving to the next batch. `total_loss` accumulates each batch's loss, and the function returns the updated `(weight, bias)` along with `total_loss / n_batches`, the average loss across the whole epoch.
