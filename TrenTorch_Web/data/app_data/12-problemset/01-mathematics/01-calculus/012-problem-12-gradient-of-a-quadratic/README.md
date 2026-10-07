---
name: problem-12-gradient-of-a-quadratic
title: 'Gradient of a Quadratic'
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Calculus'
topic: 'calculus'
hint: 'use (A+Aᵀ)x/2 + b'
tools: [NumPy]
---

## Statement

Return the gradient of 0.5*xᵀAx + bᵀx. Implement `solve(...)` so that it returns the required result exactly. Treat the task as an implementation contract rather than an open-ended modeling exercise.

**Topic:** calculus.

### Examples

Input: solve([[2.0, 0.0], [0.0, 2.0]], [1.0, 1.0], [0.0, 0.0])
Output: [2.0, 2.0]
Explanation: with A already symmetric, the gradient 0.5*(A+A^T)@x + b reduces to A@x + b = [2.0, 2.0].

Input: solve([[1.0, 2.0], [2.0, 1.0]], [1.0, -1.0], [0.0, 0.0])
Output: [-1.0, 1.0]
Explanation: for symmetric A, the gradient is A@x = [1*1+2*-1, 2*1+1*-1] = [-1.0, 1.0].

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

### What is Gradient of a Quadratic?

Gradient of a Quadratic is the specific computational form of **calculus** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why Gradient of a Quadratic is Necessary

- The operation must preserve the mathematical object being represented.
- Numerical implementations need explicit handling of scale, zero values, or singular cases.
- The result is used downstream by learning algorithms, so small computational errors can propagate.

### The Process / Mechanism

Represent the inputs in their mathematical form, compute the required intermediate quantities, then return the requested scalar, vector, matrix, or estimate. Check boundary cases such as zero norm, singular matrices, empty samples, or finite precision.

### Mathematical Representation

For inputs \(x\) and parameters required by the task, compute the requested quantity \(g(x)\) using the stated definition. When an average is required, \(\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i\); when a squared norm is required, \(\|x\|_2^2=\sum_i x_i^2\).

### Worked Example

For the first example, identify the inputs, compute the intermediate quantities in the order described by the mechanism, and only then form the final result. For the boundary example, apply the same rules without changing the algorithm; the edge case should fall out of the definition rather than from an unrelated special-case output.

## Explanation

### Why This Solution Works

The reference implementation follows the problem definition in the same order as the mechanism above. It computes the required intermediate state once, uses explicit boundary checks where division, normalization, sampling, or masking could otherwise become undefined, and returns only the requested result. This matters because a superficially similar implementation can produce the wrong shape, leak held-out statistics, mishandle a zero denominator, or change a boundary condition.

### Complexity and Optimization

The shown implementation uses the simplest asymptotic structure that matches the task. Vectorized NumPy operations move inner loops into optimized array kernels where that is natural; explicit loops remain where the algorithm itself is sequential or where clarity is more important than micro-optimization. The usual optimization is to avoid recomputing distances, norms, masks, or reductions that can be cached once. Space is dominated by the output and any intermediate arrays required by the stated operation. Do not replace the reference with an optimization that changes numerical semantics or makes the implementation harder to verify.

---
