---
name: problem-107-anomaly-z-score
title: 'Anomaly Z-Score'
tags: [problemset, unsupervised-ml, anomaly-detection]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'anomaly detection'
hint: 'standardize using training mean and std'
tools: [NumPy]
---

## Statement

Flag observations whose absolute z-score exceeds a threshold. Implement `solve(...)` so that it returns the required result exactly. Treat the task as an implementation contract rather than an open-ended modeling exercise.

**Topic:** anomaly detection.

### Examples

Input: a small valid example with two records
Output: the expected transformed result
Explanation: the implementation applies the stated rule to each record.

Input: an edge case at the stated boundary
Output: the boundary result
Explanation: the implementation handles the boundary without changing the contract.

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

### Why This Solution Works

The reference implementation follows the problem definition in the same order as the mechanism above. It computes the required intermediate state once, uses explicit boundary checks where division, normalization, sampling, or masking could otherwise become undefined, and returns only the requested result. This matters because a superficially similar implementation can produce the wrong shape, leak held-out statistics, mishandle a zero denominator, or change a boundary condition.

### Complexity and Optimization

The shown implementation uses the simplest asymptotic structure that matches the task. Vectorized NumPy operations move inner loops into optimized array kernels where that is natural; explicit loops remain where the algorithm itself is sequential or where clarity is more important than micro-optimization. The usual optimization is to avoid recomputing distances, norms, masks, or reductions that can be cached once. Space is dominated by the output and any intermediate arrays required by the stated operation. Do not replace the reference with an optimization that changes numerical semantics or makes the implementation harder to verify.

---
