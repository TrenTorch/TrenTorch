---
name: instance-based-probabilistic-gaussian-processes
title: 'Note: Gaussian Processes, a distribution over functions instead of over parameters'
tags: [classical-ml, probabilistic, gaussian-processes]
difficulty: Intermediate
---

## Statement

Implement:

```python
def rbf_kernel(input_a: np.ndarray, input_b: np.ndarray, length_scale: float, variance: float) -> np.ndarray: ...
def gp_predict(input_train, targets_train, input_test, length_scale, variance, noise) -> tuple[np.ndarray, np.ndarray]: ...
```

- `gp_predict` returns both a mean prediction _and_ a variance (uncertainty) at every test point, this is the whole point of a Gaussian Process, not an add-on.

## Theory

Every model in this curriculum so far learns a fixed, finite set of parameters, `weight`/`bias`, or a tree's structure, from the training data, then uses only those parameters to predict. A Gaussian Process (GP) is a genuinely different kind of model: instead of committing to one function described by a handful of parameters, it maintains a _distribution over every function_ consistent with the training data, and predicts by averaging over all of them, weighted by how well each one fits.

That sounds abstract, but it reduces to closed-form linear algebra for regression. A GP is defined entirely by a **kernel**, a function that says how correlated two points' outputs should be, based on how similar the points themselves are. The RBF kernel used here says "points close together in input space should have similar outputs, points far apart shouldn't," and its `length_scale` controls what "close" means:

```text
k(x_a, x_b) = variance * exp( -0.5 * ||x_a - x_b||^2 / length_scale^2 )
```

Given training points and a kernel, the GP posterior at new test points is:

```text
mean       = K(test, train) @ K(train, train)^-1 @ targets_train
covariance = K(test, test) - K(test, train) @ K(train, train)^-1 @ K(train, train, test)
```

`mean` is the GP's best single prediction, a weighted combination of the training targets, weighted by how similar (under the kernel) each training point is to the query. `covariance`'s diagonal gives a genuine uncertainty estimate, per test point, for free: far from any training data, the kernel similarities are all small, `K(test,train)` contributes little, and the variance stays close to the prior variance (high uncertainty). Near training points, the kernel pulls the variance down toward `0` (low uncertainty), the model is confident where it has evidence and honestly uncertain where it doesn't. None of the earlier models in this curriculum produce that second number at all.

`noise` (added to `K(train, train)`'s diagonal) accounts for the training targets themselves being noisy measurements, not exact function values, without it, the GP would try to pass exactly through every training point, fitting the noise along with the signal.

## Explanation

`rbf_kernel` uses the same broadcasting shape as `01-knn`'s `pairwise_distances` (`input_a[:, None, :] - input_b[None, :, :]`), squared and summed over the feature axis, then plugged into the RBF formula, `variance * exp(-0.5 * squared_distance / length_scale**2)`.

`gp_predict` builds the three kernel matrices Theory names: `k_train_train` gets `noise * np.eye(n_train)` added to its diagonal (the noise term), `k_train_test` and `k_test_test` don't, noise only applies to the actual training observations, not to the kernel's belief about how test points relate to each other or to training points.

`np.linalg.inv(k_train_train)` is computed once and reused for both `mean` and `covariance`, the same inverse appears in both formulas. `mean = k_train_test.T @ k_train_train_inv @ targets_train` and `covariance = k_test_test - k_train_test.T @ k_train_train_inv @ k_train_test` are the posterior formulas directly. `np.clip(np.diag(covariance), 0.0, None)` guards against floating-point error occasionally producing a variance of `-1e-16` instead of exactly `0`, a real variance can never be negative.
