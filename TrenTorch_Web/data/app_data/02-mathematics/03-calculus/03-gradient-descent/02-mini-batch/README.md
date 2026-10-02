---
name: math-mini-batch-gradient-descent
title: Mini-Batch
tags: [calculus, optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-standard` computes every update from the gradient of the loss over the whole training set. That is exact, but on a dataset with millions of rows a single step means reading every row once, and the model only moves after all of them have been seen. Mini-batch gradient descent keeps the same walk-downhill idea and changes one thing: each update uses the gradient from a small random subset of the data, so the model moves many times per pass through the data. This question fits a linear model to a small dataset that way.

### From theory to code

Implement `mse_gradient(X, y, w)`, the gradient of the mean squared error for a linear model, then `make_batches(num_samples, batch_size, rng)`, which shuffles the sample indices and cuts them into batches, then `mini_batch_gradient_descent(X, y, w0, learning_rate, batch_size, num_epochs, rng)`, which runs the full loop and returns every intermediate weight vector. The signatures and docstrings are already in the editor.

### Constraints

- `X` has shape `(m, d)`, `y` has shape `(m,)`, and `w` has shape `(d,)`. The model predicts `X @ w` and the loss is the mean of the squared residuals.
- `mse_gradient` must average over the rows it is given, so it works unchanged for a full dataset, a batch, or a single row.
- `make_batches` draws exactly one shuffle per call with `rng.permutation(num_samples)`. Every index appears exactly once, every batch except possibly the last has `batch_size` indices, and the last batch holds the remainder.
- `mini_batch_gradient_descent` draws a fresh shuffle at the start of every epoch and makes one update per batch. It returns a list of length `1 + num_epochs * ceil(m / batch_size)`: `w0` followed by the weights after each update.
- The inputs `X`, `y` and `w0` must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

The gradient of `mean((X @ w - y) ** 2)` with respect to `w` is a matrix-vector product: the transposed design matrix times the residual vector, scaled by `2 / len(y)`.

</details>

<details>
<summary>Hint 2</summary>

Slicing a shuffled index array with `order[start:start + batch_size]` already handles the shorter final batch, because a slice past the end just stops.

</details>

<details>
<summary>Hint 3</summary>

The loop is two nested loops: epochs on the outside, batches on the inside. Each inner iteration is one `01-standard` step, with the batch's gradient in place of the full gradient.

</details>

## Theory

### The simple version

Imagine polling a city to find out how people feel about a new policy. Asking every resident gives the exact answer but takes forever. Asking a random handful gives an answer that is slightly off, but you get it almost immediately, and if you keep asking different handfuls the errors tend to cancel out. Mini-batch gradient descent does exactly this with the gradient: each step is computed from a random handful of training rows, which is a noisy but cheap estimate of the true downhill direction.

### The formula

For a linear model with loss $L(w) = \frac{1}{m}\sum_{i=1}^{m}(x_i \cdot w - y_i)^2$, the full gradient is

$$
\nabla L(w) = \frac{2}{m} X^\top (Xw - y)
$$

A mini-batch update replaces the full dataset with a batch $B$ of $b$ rows and averages over the batch instead:

$$
w_{t+1} = w_t - \eta \, g_B(w_t), \qquad g_B(w) = \frac{2}{b} X_B^\top (X_B w - y_B)
$$

- `η` is the learning rate, exactly as in `01-standard`.
- `X_B` and `y_B` are the rows of `X` and entries of `y` whose indices are in the batch.
- Dividing by the batch size `b` (not by `m`) keeps the step the same size whatever the batch size is.
- An **epoch** is one full pass in which every row lands in exactly one batch. Shuffling at the start of each epoch gives every batch a different mix of rows each time.

### Why a random batch still points downhill

If the batch is drawn uniformly at random, the batch gradient is an **unbiased** estimate of the full gradient: its average over all possible batches is exactly $\nabla L(w)$. Any single batch is off by some noise, and that noise shrinks as the batch grows. This is the whole trade-off: a small batch is cheap per step but jittery, a large batch is smooth but costly per step. Setting the batch size equal to `m` recovers `01-standard` exactly, because the average of the gradient over every row is the full gradient no matter how the rows are ordered.

### Why the jitter is not all bad

The noise means the path wobbles instead of sliding smoothly into the bottom of a valley. That wobble can knock the weights out of shallow dips and saddle points that a perfectly smooth path would settle in, and with a fixed learning rate the weights end up hovering around the minimum rather than landing exactly on it. Practical training shrinks the learning rate over time to tighten that hover.

### How PyTorch actually implements this

`torch.utils.data.DataLoader(dataset, batch_size=b, shuffle=True)` is `make_batches` run fresh every epoch, and the loop `for xb, yb in loader: loss = ...; loss.backward(); optimizer.step()` is `mini_batch_gradient_descent`. `torch.optim.SGD` applies the plain update `param -= lr * param.grad` to whatever batch it was just given, so despite the name it is a mini-batch optimizer in almost every real training script.

## Explanation

`mse_gradient` returns `2 * X.T @ (X @ w - y) / len(y)`, a direct translation of the formula that works for any number of rows because it divides by the number of rows it receives. `make_batches` takes one `rng.permutation` and slices it in steps of `batch_size`, so the final slice is automatically the shorter remainder and every index appears exactly once. `mini_batch_gradient_descent` copies `w0` into a float array so the caller's data is never modified, then for each epoch asks `make_batches` for a fresh shuffle and applies one update per batch, appending a copy of the weights after each update so the returned trajectory does not alias a single array.
