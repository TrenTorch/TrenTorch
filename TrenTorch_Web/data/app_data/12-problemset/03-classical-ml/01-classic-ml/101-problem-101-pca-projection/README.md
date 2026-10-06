---
name: problem-101-101-pca-projection
title: 'PCA Projection'
tags: [problemset, pca]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'pca'
---

## Statement

PCA projection is a linear coordinate change: for centered row data X and component matrix V, the retained coordinates are Z = X V[:, :k]. Implement `solve(X, components, k)` and return the specified value without printing or reading from standard input. The arguments are passed directly to the Python function.

### Input Format

Call the function directly. For example:

```python
solve([[1,2],[3,4]], [[1,0],[0,1]], 1)
```

The argument order and defaults are part of the function signature.

### Output Format

Return the computed Python value. The return value must match the documented numeric values, shapes, and container structure; do not print it.

### Constraints

- Numeric inputs are finite. Arrays and sequences contain at most 100,000 elements; matrix dimensions are at most 512 per axis.
- Shapes and parameter values must satisfy the operation (for example, compatible matrix dimensions and positive window/stride sizes).
- Scalar thresholds, temperatures, probabilities, and rates follow their mathematical domain stated in the problem.
- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).

### Examples

**Example 1**

**Input**

```python
solve([[1,2],[3,4]], [[1,0],[0,1]], 1)
```

**Output**

```text
[[1], [3]]
```

**Example 2**

**Input**

```python
solve([[-1,2]], [[0,1],[1,0]], 2)
```

**Output**

```text
[[2, -1]]
```

### Hints

<details><summary>Hint 1 — identify the operation</summary>

PCA projection is a linear coordinate change: for centered row data X and component matrix V, the retained coordinates are Z = X V[:, :k].

</details>

<details><summary>Hint 2 — apply the definition</summary>

PCA projection is a linear coordinate change: for centered row data X and component matrix V, the retained coordinates are Z = X V[:, :k].

</details>

<details><summary>Hint 3 — check boundaries</summary>

Use the supplied inputs as-is, preserve the requested shape and type, and handle the stated zero or endpoint cases using the same mathematical definition.

</details>

## Theory

The principal components are the columns of $V$, ordered by how much variance they explain. Projecting centered data onto the first $k$ of them gives the coordinates $Z = X V_{:,1:k}$, a rank-$k$ view of the data that keeps as much variance as any $k$ directions can.

## Explanation

Convert `X` and `components` to arrays, keep the first `k` columns of `components`, and multiply: `X @ components[:, :k]`. The result has one row per sample and `k` columns.
