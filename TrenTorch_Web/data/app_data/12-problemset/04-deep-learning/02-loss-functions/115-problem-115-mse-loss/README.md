---
name: problem-115-mse-loss
title: 'MSE Loss'
tags: [problemset, dl-core, loss-functions]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Loss Functions'
topic: 'loss functions'
hint: 'average squared residual'
tools: [NumPy]
---

## Statement

Compute mean squared error for a regression output. Implement `solve(...)` so that it returns the required result exactly. Treat the task as an implementation contract rather than an open-ended modeling exercise.

**Topic:** loss functions.

### Examples

Input: y=[1,3], pred=[2,2]
Output: 1.0
Explanation: squared errors are 1 and 1, so their mean is 1.

Input: y=[2,2], pred=[2,2]
Output: 0.0
Explanation: every residual is zero.

### Hint

<details><summary>Hint</summary>
average squared residual
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

### What is MSE Loss?

MSE Loss is the specific computational form of **loss functions** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why MSE Loss is Necessary

- Each layer transforms a representation while preserving a differentiable path for learning.
- The backward pass must apply the chain rule in the reverse order of the forward operations.
- Numerical stability matters because exponentials, norms, and products can overflow or underflow.

### The Process / Mechanism

Compute the forward transformation, cache only what the backward computation needs, then propagate gradients through each operation in reverse order.

### Mathematical Representation

For a layer \(z=f(x;\theta)\) and upstream gradient \(\partial L/\partial z\), the chain rule gives \(\frac{\partial L}{\partial x}=\frac{\partial L}{\partial z}\frac{\partial z}{\partial x}\).

### Worked Example

For the first example, identify the inputs, compute the intermediate quantities in the order described by the mechanism, and only then form the final result. For the boundary example, apply the same rules without changing the algorithm; the edge case should fall out of the definition rather than from an unrelated special-case output.

## Explanation

### Why This Solution Works

The reference implementation follows the problem definition in the same order as the mechanism above. It computes the required intermediate state once, uses explicit boundary checks where division, normalization, sampling, or masking could otherwise become undefined, and returns only the requested result. This matters because a superficially similar implementation can produce the wrong shape, leak held-out statistics, mishandle a zero denominator, or change a boundary condition.

### Complexity and Optimization

The shown implementation uses the simplest asymptotic structure that matches the task. Vectorized NumPy operations move inner loops into optimized array kernels where that is natural; explicit loops remain where the algorithm itself is sequential or where clarity is more important than micro-optimization. The usual optimization is to avoid recomputing distances, norms, masks, or reductions that can be cached once. Space is dominated by the output and any intermediate arrays required by the stated operation. Do not replace the reference with an optimization that changes numerical semantics or makes the implementation harder to verify.

---
