---
name: numpy-vector-norms
title: np.linalg.norm
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

Implement functions computing vector norms both from their mathematical definition and using `np.linalg.norm`.

## Theory

A **norm** measures the "size" of a vector. The **Euclidean (L2) norm**:

$$
\|v\|_2 = \sqrt{\sum_{k=0}^{n-1} v_k^2}
$$

```python
v = np.array([3, 4])
np.linalg.norm(v)     # 5.0 — sqrt(3^2 + 4^2)
```

`np.linalg.norm` defaults to L2 but supports other norms via `ord` — L1 (sum of absolute values) and infinity (max absolute value).

**Normalizing a vector to length 1** — dividing every element by its own norm produces a unit vector pointing the same direction:

```python
v = np.array([3, 4])
unit_v = v / np.linalg.norm(v)     # [0.6, 0.8]
np.linalg.norm(unit_v)               # 1.0
```

## Explanation

`l2_norm_from_scratch` computes `np.sqrt(np.sum(v ** 2))` directly. `l2_norm_builtin` is `np.linalg.norm(v)`. `normalize_vector` returns `v / np.linalg.norm(v)`, a new array — `v` itself is never mutated, since division always produces a fresh array (Module 6's element-wise-op copy rule).
