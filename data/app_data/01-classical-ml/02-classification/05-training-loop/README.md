---
name: classification-training-loop
title: Full Training Loop
tags: [classical-ml, classification, training-loop]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The earlier classification questions define a score, turn it into a probability, and determine the direction to correct it. Training is the repeated process that connects those pieces so a classifier learns its parameters from all examples.

### From theory to code

Implement `train_logistic_regression` by reusing `linear`, `sigmoid`, `bce_gradient`, and `gd_step` in their forward-to-update order.

### Constraints

- `input` is `(batch_size, in_features)` and binary `target` is `(batch_size,)`.
- Return `(weight, bias)` with shapes `(1, in_features)` and `(1,)`.
- Initialize both parameters to zero and reshape targets once to `(batch_size, 1)`.
- Run exactly `epochs` full-batch updates; zero epochs returns the initialization.
- Do not reimplement the imported helpers or use loops over samples.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

The forward pass has two stages: a linear score followed by a probability activation.

</details>

<details><summary>Hint 2</summary>

Within each epoch, pass `sigmoid(linear(...))` and the reshaped targets to `bce_gradient`, then hand its results to `gd_step`.

</details>

## Theory

### The simple version

Logistic training repeatedly turns feature evidence into confidence, compares that confidence with the label, and nudges the evidence weights in the direction that makes future confidence more appropriate.

### The formula

```text
W_0 = 0; b_0 = 0; Y = target.reshape(-1, 1)
p_t = sigmoid(linear(input, W_t, b_t))
(dW_t, db_t) = bce_gradient(input, p_t, Y)
(W_{t+1}, b_{t+1}) = gd_step(W_t, b_t, dW_t, db_t, lr)
```

Repeat the final three lines `epochs` times.

### How PyTorch actually implements this

Context only, untested by your submission: logistic models commonly use `torch.nn.Linear`, `torch.nn.BCEWithLogitsLoss`, and an optimizer; autograd replaces the explicit `bce_gradient` call.

## Explanation

The initialization and `target_2d = target.reshape(-1, 1)` match the existing single-output shape convention. In every loop iteration, `linear` produces raw scores and `sigmoid` produces `p`; `bce_gradient` returns the matching row-vector and one-element gradients; `gd_step` applies them. No calculation runs when `epochs` is zero.
