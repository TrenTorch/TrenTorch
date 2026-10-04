---
name: gradient-check-one-parameter-company-250
title: "gradient-check-one-parameter — Google case"
tags: [problemset, dl-core, backpropagation, google]
difficulty: Intermediate
kind: problemset
relatedModule: "part-dl-training|Optimization"
topic: "Optimization"
caseCompany: "Google"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
---

## Statement

Google-inspired optimization team is debugging a custom differentiable component whose analytical gradient may be wrong. You need to compute a numerical finite-difference gradient for one parameter so the team can compare it with the implementation.

### Input Format

```python
solve(f, x, analytic, h)
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
solve(...)
```

**Output**
```text
See the function's return value for this input.
```

The output is produced by running the reference solution with these arguments.

### Hints

<details><summary>Hint</summary>

Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.

</details>

## Theory

### The simple version

**gradient checking** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

\frac{\partial f}{\partial x_i}\approx\frac{f(x+h e_i)-f(x-h e_i)}{2h}.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Gradient checking catches implementation mistakes by comparing backpropagation against an independent numerical approximation.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(1) function evaluations for one coordinate, though each evaluation costs the full loss computation.
