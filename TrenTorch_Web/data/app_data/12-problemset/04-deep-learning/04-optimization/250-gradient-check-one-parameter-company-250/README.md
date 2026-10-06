---
name: gradient-check-one-parameter-company-250
title: 'gradient-check-one-parameter — Google case'
tags: [problemset, dl-core, backpropagation, google]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'Google'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
---

## Statement

Google-inspired optimization team is debugging a custom differentiable component whose analytical gradient may be wrong. You need to compute a numerical finite-difference gradient for one parameter so the team can compare it with the implementation.

### Input Format

```text
See the `solve(...)` signature in the reference implementation. Arguments are ordinary Python values or NumPy arrays; no stdin/stdout parsing is used.
```

### Output Format

```text
Return exactly the scalar, vector, matrix, tuple, or other Python object described by the statement.
```

### Constraints

- Inputs must satisfy the dimensions and value assumptions stated by the problem.
- Use finite floating-point values unless the statement explicitly permits another case.
- Input sizes are bounded so the reference implementation completes comfortably within the platform limit.
- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).

### Example

**Input**
```text
[1.5], [3.0] for f(x)=x^2
```

**Output**
```text
(3.0,3.0,0.0)
```

**Explanation:** The centered difference agrees with the derivative 2x at x=1.5.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
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
