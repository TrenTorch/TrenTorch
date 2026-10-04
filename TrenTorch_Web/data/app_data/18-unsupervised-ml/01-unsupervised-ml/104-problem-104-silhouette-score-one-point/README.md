---
name: problem-104-silhouette-score-one-point
title: "Silhouette Score One Point"
tags: [problemset, unsupervised-ml, clustering-metrics]
difficulty: Intermediate
kind: problemset
relatedModule: "part-classical-unsupervised|Classic ML"
topic: "clustering metrics"
hint: "use (b-a)/max(a,b)"
tools: [NumPy]
---

## Statement



### Input Format

```python
solve(intra, nearest)
```

Arguments are passed directly to the function; there is no stdin/stdout parsing.

### Output Format

Return the value computed by `solve`; do not print it.

### Constraints

- Vector inputs contain at most 100,000 elements; matrix dimensions are at most 512 per axis.
- Inputs must satisfy the shapes and finite-value assumptions in the function signature.

- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).

### Example

**Example 1**

**Input**
```python
solve(...)
```

**Output**
```text
See the function's return value for this input.
```

The output is produced by running the reference solution with these arguments.

### Hints

<details><summary>Hint</summary>

use (b-a)/max(a,b)

</details>

## Theory

### What is Silhouette Score One Point?

Silhouette Score One Point is the specific computational form of **clustering metrics** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why Silhouette Score One Point is Necessary

- There may be no target label, so structure must be inferred from distances, densities, or likelihoods.
- Scale and representation directly affect the discovered structure.
- Degenerate clusters or zero-variance dimensions must have defined behavior.

### The Process / Mechanism

Measure similarity or density, assign observations to structures, update the structure when the algorithm is iterative, and stop when the specified criterion is met.

### Mathematical Representation

For Euclidean distance, \(d(x,c)=\sqrt{\sum_j(x_j-c_j)^2}\). Many unsupervised objectives minimize or maximize an aggregate of such local quantities.

### Worked Example

For the first example, identify the inputs, compute the intermediate quantities in the order described by the mechanism, and only then form the final result. For the boundary example, apply the same rules without changing the algorithm; the edge case should fall out of the definition rather than from an unrelated special-case output.

## Explanation

The reference implementation follows the contract for Silhouette Score One Point and returns the computed value without printing.
