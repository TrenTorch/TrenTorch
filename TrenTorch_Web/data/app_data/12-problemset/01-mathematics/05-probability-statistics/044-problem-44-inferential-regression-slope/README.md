---
name: problem-44-inferential-regression-slope
title: 'Inferential Regression Slope'
tags: [problemset, data-stats-for-ds, regression-for-inference]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'regression for inference'
hint: 'center x and y and use covariance over variance'
tools: [NumPy]
---

## Statement

Compute the least-squares slope and intercept for one predictor. Implement `solve(...)` so that it returns the required result exactly. Treat the task as an implementation contract rather than an open-ended modeling exercise.

**Topic:** regression for inference.

### Examples

Input: a small valid example with two records
Output: the expected transformed result
Explanation: the implementation applies the stated rule to each record.

Input: an edge case at the stated boundary
Output: the boundary result
Explanation: the implementation handles the boundary without changing the contract.

### Hint

<details><summary>Hint</summary>
center x and y and use covariance over variance
</details>

### Requirements

- Return the exact object described by the task; do not add logging or explanatory text to the return value.
- Use deterministic behavior for ties and boundary cases.
- Handle the explicit edge cases in the constraints without special-casing the visible examples.

### Input Format

```text
Arguments are passed directly to the typed Python function signature; no stdin/stdout parsing is used.
```

### Output Format

```text
Return the exact Python value described by the statement.
```

### Constraints

- Input sizes are bounded by the examples and function contract.
- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).

- Inputs contain finite numeric values unless the problem explicitly states otherwise.
- n <= 10,000 and feature dimension <= 512.
- Define behavior for empty inputs, singleton inputs, and zero denominators where applicable.

## Theory

### What is Inferential Regression Slope?

Inferential Regression Slope is the specific computational form of **regression for inference** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why Inferential Regression Slope is Necessary

- Data must be transformed without leaking information from held-out observations.
- The transformation must define behavior for missing, constant, imbalanced, or boundary data.
- Statistical summaries should correspond to the population and estimator specified by the task.

### The Process / Mechanism

Fit any required statistics on the permitted training/sample data, apply the transformation deterministically, and keep edge cases explicit. For inferential tasks, compute the estimator first and then its uncertainty or test statistic.

### Mathematical Representation

For an estimator based on observations \(x_1,\ldots,x_n\), the sample mean is \(\bar{x}=\frac{1}{n}\sum_i x_i\), and a standardized value is \(z_i=\frac{x_i-\bar{x}}{s}\) when \(s>0\).

### Worked Example

For the first example, identify the inputs, compute the intermediate quantities in the order described by the mechanism, and only then form the final result. For the boundary example, apply the same rules without changing the algorithm; the edge case should fall out of the definition rather than from an unrelated special-case output.

## Explanation

### Why This Solution Works

The reference implementation follows the problem definition in the same order as the mechanism above. It computes the required intermediate state once, uses explicit boundary checks where division, normalization, sampling, or masking could otherwise become undefined, and returns only the requested result. This matters because a superficially similar implementation can produce the wrong shape, leak held-out statistics, mishandle a zero denominator, or change a boundary condition.

### Complexity and Optimization

The shown implementation uses the simplest asymptotic structure that matches the task. Vectorized NumPy operations move inner loops into optimized array kernels where that is natural; explicit loops remain where the algorithm itself is sequential or where clarity is more important than micro-optimization. The usual optimization is to avoid recomputing distances, norms, masks, or reductions that can be cached once. Space is dominated by the output and any intermediate arrays required by the stated operation. Do not replace the reference with an optimization that changes numerical semantics or makes the implementation harder to verify.

---

# Classical ML
