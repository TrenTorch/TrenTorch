---
name: cosine-learning-rate-company-240
title: 'cosine-learning-rate — Adobe case'
tags: [problemset, dl-training-theory, learning-rate-schedules, adobe]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Adobe'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
---

## Statement

Adobe-inspired model-training pipeline changes its learning rate over the course of a training schedule. You need to calculate the cosine-decayed learning rate at a requested training step so the scheduler matches the experiment configuration.

### Input Format

```python
solve(t, T, lr_max, lr_min)
```

Arguments are passed directly to the function; there is no stdin/stdout parsing.

### Output Format

Return the value computed by `solve`; do not print it.

### Constraints

- Inputs must satisfy the dimensions and value assumptions stated by the problem.
- Use finite floating-point values unless the statement explicitly permits another case.
- Input sizes are bounded so the reference implementation completes comfortably within the platform limit.

- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).

### Example

**Example 1**

**Input**

```python
solve(1, 1, 1, 1)
```

**Output**

```text
1.0
```

The output is produced by running the reference solution with these arguments.

**Example 2**

**Input**

```python
solve(1, 1, 1, 1)
```

**Output**

```text
1.0
```

The output is produced by running the reference solution with these arguments.

### Hints

<details><summary>Hint</summary>

Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.

</details>

## Theory

### The simple version

**cosine schedule** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

\eta_t=\eta_{min}+\frac12(\eta_{max}-\eta_{min})(1+\cos(\pi t/T)).

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Cosine decay lowers the step size smoothly rather than changing it abruptly at hand-picked boundaries.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(1) time and space.
