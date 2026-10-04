---
name: problem-107-anomaly-z-score
title: "Anomaly Z-Score"
tags: [problemset, unsupervised-ml, anomaly-detection]
difficulty: Advanced
kind: problemset
relatedModule: "part-classical-unsupervised|Classic ML"
topic: "anomaly detection"
hint: "standardize using training mean and std"
tools: [NumPy]
---

## Statement



### Input Format

```python
solve(x, threshold)
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

standardize using training mean and std

</details>

## Theory

### What is Anomaly Z-Score?

Anomaly Z-Score is the specific computational form of **anomaly detection** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why Anomaly Z-Score is Necessary

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

The reference implementation follows the contract for Anomaly Z-Score and returns the computed value without printing.
