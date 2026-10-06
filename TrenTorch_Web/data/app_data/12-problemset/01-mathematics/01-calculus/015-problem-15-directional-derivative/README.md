---
name: problem-15-directional-derivative
title: 'Directional Derivative'
tags: [problemset, maths-stats-for-ml, calculus]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Calculus'
topic: 'calculus'
hint: 'normalize the direction before taking the dot product with the gradient'
tools: [NumPy]
---

## Statement

Compute the directional derivative of a scalar function. Implement `solve(...)` so that it returns the required result exactly. Treat the task as an implementation contract rather than an open-ended modeling exercise.

**Topic:** calculus.

### Examples

Input: f(x)=x², x=3, h=1e-5
Output: approximately 6
Explanation: the centered finite difference approximates the analytic derivative 2x.

Input: f(x)=x³, x=2, h=1e-5
Output: approximately 12
Explanation: the derivative is 3x².

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

### What is Directional Derivative?

Directional Derivative is the specific computational form of **calculus** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why Directional Derivative is Necessary

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
