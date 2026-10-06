---
name: problem-143-early-stopping
title: 'Early Stopping'
tags: [problemset, dl-training-theory, regularization]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'regularization'
hint: 'reset patience on strict improvement'
tools: [NumPy]
---

## Statement

Track validation loss and stop after patience bad epochs. Implement `solve(...)` so that it returns the required result exactly. Treat the task as an implementation contract rather than an open-ended modeling exercise.

**Topic:** regularization.

### Examples

Input: a small valid example with two records
Output: the expected transformed result
Explanation: the implementation applies the stated rule to each record.

Input: an edge case at the stated boundary
Output: the boundary result
Explanation: the implementation handles the boundary without changing the contract.

### Hint

<details><summary>Hint</summary>
reset patience on strict improvement
</details>

### Requirements

- Return the exact object described by the task; do not add logging or explanatory text to the return value.
- Use deterministic behavior for ties and boundary cases.
- Handle the explicit edge cases in the constraints without special-casing the visible examples.
- Do not use statistics from held-out data unless the task explicitly asks for them.

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

### What is Early Stopping?

Early Stopping is the specific computational form of **regularization** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why Early Stopping is Necessary

- Optimization changes parameters according to gradients and a schedule.
- Training stability depends on gradient scale, regularization, and numerical precision.
- Validation behavior, not training loss alone, determines whether additional optimization is useful.

### The Process / Mechanism

Read the current parameter state and gradient statistics, compute the optimizer or schedule update, apply any clipping/regularization rules, and return the updated state.

### Mathematical Representation

A basic parameter update is \(\theta_{t+1}=\theta_t-\eta_t g_t\), where \(\eta_t\) is the current learning rate and \(g_t\) is the gradient.

### Worked Example

For the first example, identify the inputs, compute the intermediate quantities in the order described by the mechanism, and only then form the final result. For the boundary example, apply the same rules without changing the algorithm; the edge case should fall out of the definition rather than from an unrelated special-case output.

## Explanation

### Why This Solution Works

The reference implementation follows the problem definition in the same order as the mechanism above. It computes the required intermediate state once, uses explicit boundary checks where division, normalization, sampling, or masking could otherwise become undefined, and returns only the requested result. This matters because a superficially similar implementation can produce the wrong shape, leak held-out statistics, mishandle a zero denominator, or change a boundary condition.

### Complexity and Optimization

The shown implementation uses the simplest asymptotic structure that matches the task. Vectorized NumPy operations move inner loops into optimized array kernels where that is natural; explicit loops remain where the algorithm itself is sequential or where clarity is more important than micro-optimization. The usual optimization is to avoid recomputing distances, norms, masks, or reductions that can be cached once. Space is dominated by the output and any intermediate arrays required by the stated operation. Do not replace the reference with an optimization that changes numerical semantics or makes the implementation harder to verify.

---
