---
name: linear-regression-training-loop
title: Full Linear Regression Training Loop
tags: [classical-ml, linear-regression, training-loop]
difficulty: Intermediate
---

## Statement

Implement:

```python
def train_linear_regression(
    input: np.ndarray,
    target: np.ndarray,
    lr: float,
    epochs: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    input:  shape (batch_size, in_features)
    target: shape (batch_size,), one target value per sample
    lr: learning rate
    epochs: number of full-batch gradient-descent steps

    Returns:
        weight: shape (1, in_features)
        bias: shape (1,)
    """
```

Your function should:

1. Initialize `weight` to zeros, shape `(1, in_features)`, and `bias` to zeros, shape `(1,)`. One output feature, matching `target`.
2. Reshape `target` once, up front, to `(batch_size, 1)`, the shape `01-hypothesis-function`'s `linear` actually produces, never leave it `(batch_size,)` and let it silently broadcast against a prediction later.
3. Repeat, `epochs` times: compute gradients with `03-mse-gradient`'s `mse_gradient`, then apply one step with `04-gd-step`'s `gd_step`.
4. Return the final `weight`, `bias`.

Use the functions you already implemented in the earlier questions rather than reimplementing their logic inside the training loop.

## Theory

We now have every individual piece required to train the model.

Training simply means repeating the same process many times:

```text
initialize weight, bias
       ↓
   compute gradients   (mse_gradient calls linear internally)
       ↓
   update weight, bias  (gd_step)
       ↓
     repeat
```

Each repetition is called an epoch. As training progresses, the parameters should move toward values that produce smaller prediction errors.

The one new decision this question makes, that the earlier ones in this track didn't have to, is the shape of `target`. A real dataset hands you a plain `(batch_size,)` array of house prices or whatever you're predicting, one value per sample, there's no natural reason to think of it as a `(batch_size, 1)` matrix. But `mse_gradient` (and `linear` underneath it) always produce a `(batch_size, 1)` prediction for a single-output model, never squeezed. Reshape `target` once, at the boundary of this function, and every call after that is shape-safe by construction. Skip that reshape and you get the exact silent `(batch_size, 1)` vs `(batch_size,)` broadcast this curriculum has been warning about since Q1, except now it's hiding inside a loop that runs hundreds of times.

This is the basic training-loop pattern that will appear again and again in deep learning. Later, the model, loss, and optimizer may become much more complicated, but the structure is fundamentally the same.

## Explanation

`weight = np.zeros((1, input.shape[1]))`, not a hardcoded size, this is what lets the function work for any `in_features` without the caller passing it separately. `bias = np.zeros(1)`, matching `linear`'s `(out_features,)` convention for a single output feature.

`target_2d = target.reshape(-1, 1)` happens exactly once, before the loop, converting the natural `(batch_size,)` input into the `(batch_size, 1)` shape every downstream function expects. `-1` rather than a hardcoded `batch_size` for the same reason `weight`'s shape isn't hardcoded, it should work for any batch size.

The loop body is `mse_gradient` → `gd_step`, in sequence, and nothing else. No formula is reimplemented here, only wired together, every actual computation stays owned by the function that was already tested for it.
