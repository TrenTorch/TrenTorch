---
name: instance-based-probabilistic-gaussian-naive-bayes
title: 'Stretch: Gaussian Naive Bayes'
tags: [classical-ml, probabilistic, naive-bayes, stretch]
difficulty: Intermediate
---

## Statement

Implement:

```python
def gaussian_nb_fit(input: np.ndarray, labels: np.ndarray, var_smoothing: float = 1e-9) -> dict: ...
def gaussian_log_likelihood(x: np.ndarray, mean: np.ndarray, variance: np.ndarray) -> float: ...
def gaussian_nb_predict(model: dict, queries: np.ndarray) -> np.ndarray: ...
```

- `input` is real-valued this time, `02-naive-bayes-bernoulli`'s features were binary.
- Same overall shape as `02-naive-bayes-bernoulli`, only the per-feature probability model changes.

## Theory

`02-naive-bayes-bernoulli` modeled each feature as a coin flip, present or absent. Real-valued features need a different per-feature model, the classic choice is a Gaussian: for each class, each feature is assumed to follow its own normal distribution, with its own mean and variance estimated from that class's training examples.

```text
P(feature_i | class) = Gaussian(feature_i; mean_i,class, variance_i,class)
```

Naive Bayes's independence assumption still applies exactly the way `02-naive-bayes-bernoulli`'s Theory describes, `P(features | class)` is a product over independent per-feature terms, so its log is a sum, same reasoning, a different per-feature distribution:

```text
log P(features | class) = sum over features i of log Gaussian(x_i; mean_i, variance_i)
                         = sum over features i of [ -0.5*log(2*pi*variance_i) - (x_i - mean_i)^2 / (2*variance_i) ]
```

Fitting is simple: `mean_i,class` and `variance_i,class` are just the sample mean and sample variance of feature `i`, computed only from class `c`'s training rows. `var_smoothing` plays the same role `alpha` played in `02-naive-bayes-bernoulli`, a feature that happens to be exactly constant within one class would otherwise get a variance of `0`, and dividing by `0` in the Gaussian formula is at least as broken as `log(0)` was there. A small floor, a tiny fraction of the largest feature variance seen across the whole dataset, keeps every variance strictly positive.

## Explanation

`gaussian_nb_fit` computes `epsilon = var_smoothing * np.var(input, axis=0).max()` once, from the entire dataset (not per class), this is the smoothing floor added to every class's own per-feature variance. For each class, `means[c]` and `variances[c] + epsilon` are `class_input.mean(axis=0)` / `class_input.var(axis=0)`, NumPy's own per-feature statistics over just that class's rows.

`gaussian_log_likelihood` is the Gaussian log-density formula, applied elementwise across `x`/`mean`/`variance` (all shape `(n_features,)`) and summed, exactly mirroring `02-naive-bayes-bernoulli`'s log-likelihood shape, a per-feature term computed then reduced with one `np.sum`.

`gaussian_nb_predict` is unchanged in structure from `02-naive-bayes-bernoulli`'s `bernoulli_nb_predict`, score every class by `log_prior + log_likelihood`, argmax over classes, only the log-likelihood function underneath is different.
