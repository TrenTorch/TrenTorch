---
name: problem-127-average-pooling-2d
title: 'Average Pooling 2D'
tags: [problemset, dl-core, cnn-basics]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'cnn basics'
hint: 'take mean per window'
tools: [NumPy]
---

## Statement

Implement non-overlapping average pooling. Implement `solve(...)` so that it returns the required result exactly. Treat the task as an implementation contract rather than an open-ended modeling exercise.

**Topic:** cnn basics.

### Examples

Input: X=[[1,3],[2,4]], kernel=2
Output: [[4]]
Explanation: max pooling selects the largest value in the window.

Input: X=[[1,3],[2,4]], kernel=2
Output: [[2.5]]
Explanation: average pooling returns the mean of the four values.

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

### What is Average Pooling 2D?

Average Pooling 2D is the specific computational form of **cnn basics** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why Average Pooling 2D is Necessary

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
