---
name: instance-based-probabilistic-naive-bayes-bernoulli
title: 'Naive Bayes: Bernoulli log-likelihood'
tags: [classical-ml, probabilistic, naive-bayes]
difficulty: Intermediate
---

## Statement

Implement:

```python
def bernoulli_nb_fit(input: np.ndarray, labels: np.ndarray, alpha: float = 1.0) -> dict: ...
def bernoulli_log_likelihood(x: np.ndarray, feature_probs: np.ndarray) -> float: ...
def bernoulli_nb_predict(model: dict, queries: np.ndarray) -> np.ndarray: ...
```

- `input` entries are `0` or `1` (feature present/absent), the classic representation for things like "does this word appear in this document."
- `alpha` is Laplace smoothing strength, `1.0` is the standard default.

## Theory

`01-knn` predicts by comparing distances directly. Naive Bayes takes a fully probabilistic approach: model `P(class | features)` via Bayes' rule, `P(class | features) ∝ P(features | class) * P(class)`, and pick whichever class makes that product largest.

The "naive" part is the assumption that, _within_ a class, every feature is independent of every other feature. That's rarely literally true (word co-occurrence in real text is exactly the kind of thing this assumption ignores), but it makes `P(features | class)` factor into a simple product over features, which is both easy to estimate from data and easy to compute:

```text
P(features | class) = product over every feature i of P(feature_i | class)
```

For binary features, each `P(feature_i | class)` is itself a Bernoulli probability, "what fraction of class `c`'s training examples had feature `i` present." Multiplying many probabilities together underflows quickly (numbers this small vanish to `0` in floating point), so in practice everything is done in log space, sums instead of products:

```text
log P(features | class) = sum over features i of [ x_i * log(p_i) + (1 - x_i) * log(1 - p_i) ]
```

where `x_i` is `0` or `1` (this feature's actual value) and `p_i = P(feature_i = 1 | class)`. When `x_i=1` only the `log(p_i)` term contributes, when `x_i=0` only `log(1-p_i)` does, exactly the Bernoulli log-likelihood for one feature, summed across all of them.

`alpha` (Laplace smoothing) prevents a feature that happened to be `0` in every training example of some class from getting `p_i = 0` exactly, which would make `log(p_i) = -inf` and permanently rule out that class the moment the feature is ever seen as `1`, one unlucky small sample shouldn't create an absolute certainty. Adding `alpha` to the numerator and `2*alpha` to the denominator nudges every estimate slightly toward `0.5`, "genuinely unknown" rather than "impossible."

## Explanation

`bernoulli_nb_fit` computes, for each class, `log_priors[c] = log(class_count / n_samples)` (how common this class is overall) and `feature_probs[c] = (input[mask].sum(axis=0) + alpha) / (class_count + 2*alpha)`, the smoothed fraction of class `c`'s examples that had each feature present, one value per feature, computed for every feature at once via `.sum(axis=0)`.

`bernoulli_log_likelihood` is the formula above, directly: `x * np.log(feature_probs) + (1 - x) * np.log(1 - feature_probs)`, summed over the feature axis.

`bernoulli_nb_predict` scores every class as `log_prior + bernoulli_log_likelihood`, working entirely in log space means this is a sum, not a product, and picks `classes[np.argmax(scores)]`, the class Bayes' rule says is most probable given this query's features.
