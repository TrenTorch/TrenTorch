---
name: math-stochastic-gradient-descent
title: Stochastic
tags: [calculus, optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-mini-batch` showed that a gradient computed from a few rows is a cheap, noisy stand-in for the full gradient. Push that idea as far as it goes and use a single row per update. That is stochastic gradient descent: look at one training example, nudge the weights to fit it a little better, move on to the next one. The model updates `m` times per pass through the data instead of once, and every one of those updates is as cheap as an update can be. This question fits the same linear model as before, one example at a time.

### From theory to code

Implement `sample_gradient(x_i, y_i, w)`, the gradient of the squared error on a single example, then `stochastic_gradient_descent(X, y, w0, learning_rate, num_epochs, rng)`, which runs the full loop and returns every intermediate weight vector. The signatures and docstrings are already in the editor.

### Constraints

- `X` has shape `(m, d)`, `y` has shape `(m,)`, and `w0` has shape `(d,)`. `x_i` is one row of `X` with shape `(d,)` and `y_i` is its scalar target. The model predicts `x_i @ w`.
- `stochastic_gradient_descent` draws a fresh shuffle at the start of every epoch with `rng.permutation(m)` and makes one update per example, so each example is used exactly once per epoch.
- It returns a list of length `1 + num_epochs * m`: `w0` followed by the weights after each update.
- The inputs `X`, `y` and `w0` must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

For one example the loss is `(x_i @ w - y_i) ** 2`. Its gradient is the scalar residual times the example's own feature vector, doubled.

</details>

<details>
<summary>Hint 2</summary>

Iterate directly over the shuffled index array. Each pass through the inner loop is one update, which is `01-standard`'s step with a single example's gradient.

</details>

## Theory

### The simple version

Learning to throw darts by looking at your whole history of throws before every tiny adjustment would be painfully slow. A better way is to throw once, see where it landed, nudge your aim a little, and throw again. Each throw gives you a rough and slightly misleading signal, since one dart is not the whole story, but you get thousands of adjustments in the time it took to do one careful one. Stochastic gradient descent adjusts the weights after every single example.

### The formula

For a single example $(x_i, y_i)$ the loss is $\ell_i(w) = (x_i \cdot w - y_i)^2$, so its gradient is

$$
\nabla \ell_i(w) = 2\,(x_i \cdot w - y_i)\,x_i
$$

and the update is

$$
w_{t+1} = w_t - \eta \, \nabla \ell_{i_t}(w_t)
$$

where $i_t$ is the example chosen at step $t$.

- This is the mini-batch update from `02-mini-batch` with a batch size of one.
- An **epoch** is one full pass where each example is used exactly once, in a freshly shuffled order. One epoch is `m` updates.
- With no averaging there is no noise reduction at all, which is why the path is so jagged.

### Why one example still points downhill, on average

If $i_t$ is chosen uniformly at random, the single-example gradient is an unbiased estimate of the full gradient: averaged over every possible choice of example, it equals $\nabla L(w)$. Any one step can point well away from the true downhill direction, but the steps are correct on average, so the weights still drift toward the minimum. The price is variance: the weights bounce around instead of settling, and with a fixed learning rate they hover in a neighbourhood of the minimum rather than landing on it.

### The three variants side by side

| Variant                      | Examples per update | Updates per epoch | Gradient quality              |
| ---------------------------- | ------------------- | ----------------- | ----------------------------- |
| Batch (`01-standard`)        | all `m`             | 1                 | exact, smooth path            |
| Mini-batch (`02-mini-batch`) | `b`                 | `ceil(m / b)`     | slightly noisy                |
| Stochastic (this question)   | 1                   | `m`               | very noisy, cheapest per step |

Mini-batches win in practice because a batch of a few dozen rows is nearly as cheap as one row on vectorized hardware while being far less noisy.

### How PyTorch actually implements this

There is no separate "stochastic" optimizer in PyTorch. `torch.optim.SGD` applies `param -= lr * param.grad` to whatever gradient the last `loss.backward()` produced, so feeding it a `DataLoader` with `batch_size=1` gives exactly this algorithm and `batch_size=m` gives batch gradient descent. The word "stochastic" describes how the gradient was sampled, not the update rule.

## Explanation

`sample_gradient` returns `2 * (x_i @ w - y_i) * x_i`, the scalar residual scaled by the example's own feature vector, which is the single-row case of the formula in `02-mini-batch`. `stochastic_gradient_descent` copies `w0` into a float array so the caller's data is never modified, then for each epoch takes one `rng.permutation(len(y))` and updates the weights once per index in that order, appending a copy of the weights after every update so the returned trajectory does not alias a single array. Using the permutation, rather than sampling indices with replacement, is what guarantees each example is seen exactly once per epoch.
