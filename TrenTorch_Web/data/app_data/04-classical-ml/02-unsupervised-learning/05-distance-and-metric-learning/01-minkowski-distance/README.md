---
name: distance-minkowski
title: 'Minkowski distance'
tags: [classical-ml, distance, minkowski, knn, clustering]
difficulty: Beginner
---

## Statement

### One formula covers Manhattan, Euclidean and Chebyshev distance

The Minkowski distance between two vectors is `d_p(x, y) = (sum_i |x_i - y_i|^p)^(1/p)`. The exponent `p` sets the geometry: `p = 1` is Manhattan, `p = 2` is Euclidean, and `p = infinity` is the largest coordinate difference.

Implement `minkowski(x, y, p)`.

- `x` and `y` are 1-D float arrays of the same length. `p` is a real number with `p >= 1`, or `float('inf')`.
- Return the distance as a float.

### Constraints

- `x` and `y` must be 1-D and the same length. Otherwise raise `ValueError`.
- `p < 1` raises `ValueError`. Values below 1 do not satisfy the triangle inequality.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

For `p = inf`, the limit of the formula is the maximum of the absolute differences.

</details>

## Theory

For `p >= 1` the function is a metric: it is zero only at identical points, symmetric, and satisfies the triangle inequality. Its unit ball changes shape with `p`, which is why the same nearest neighbour can differ between metrics. A useful fact is that the norm is nonincreasing in `p`, so Chebyshev distance is never larger than Manhattan distance on the same pair.

### Where this shows up in production

Minkowski distances sit inside almost every nearest-neighbour search. Vector search services run Euclidean distance, sometimes with cosine similarity on normalized embeddings, and some sparse-feature systems use Manhattan distance because it is more robust to a single large feature difference. Clustering pipelines and anomaly detectors expose the exponent as a setting.

### Using it to make decisions

Start with Euclidean distance on standardized features. Use Manhattan when features are counts or sparse and one large coordinate gap should not dominate the score. Use a large `p` only when the largest single difference is the thing that matters, such as a tolerance check. Whatever you choose, standardize first: Minkowski distance treats every coordinate as equally important, so a feature measured in grams beats one measured in kilograms before scaling.

### Pros and cons

**Pros:** one formula, fast to vectorize, a metric for `p >= 1`, and the exponent gives an easy knob to test on validation data.

**Cons:** it treats all coordinates as equally important, so unscaled features dominate. In high dimensions, all pairwise distances become similar, which hurts neighbour search, and no single `p` is right for mixed data types.

## Explanation

The solution takes absolute coordinate differences and raises them to the power `p` before summing and taking the `1/p` root. The infinite case uses the maximum directly, so no special handling is needed in the caller.
