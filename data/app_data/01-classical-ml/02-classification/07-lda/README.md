---
name: classification-lda
title: Linear Discriminant Analysis (LDA)
tags: [classical-ml, classification, generative-models]
difficulty: Advanced
---

## Statement

Implement:

```python
def lda_fit(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    """
    Returns (w, b) for the linear discriminant boundary, computed from
    per-class means, one shared (pooled) covariance matrix, and class priors.
    """
```

## Theory

Q1-Q6 all learn `w, b` by gradient descent, directly fitting the boundary (discriminative: model `P(y|x)`). LDA models each class as its own Gaussian (generative: model `P(x|y)`, use Bayes' rule for `P(y|x)`).

```text
class 0 points cluster around mean₀
class 1 points cluster around mean₁
both classes share the same spread (covariance)
```

Sharing one covariance matrix is exactly what makes LDA's boundary linear too, arrived at by a completely different route.

## Explanation

`(n - 2)`, not `n`, in the pooled covariance denominator — this is Bessel's-correction-style unbiased estimation, subtracting one degree of freedom for each class's own mean already having been estimated from the data (two classes, two means, two degrees of freedom spent). Using `n` instead would systematically underestimate the true covariance and quietly bias every downstream boundary computed from it.

The `np.log(prior1/prior0)` term in `b` is what makes LDA's boundary correctly account for unequal class sizes — drop it, and a dataset with 90% class-0 points gets a boundary that ignores that base-rate information entirely.
