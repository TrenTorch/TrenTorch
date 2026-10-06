---
name: entropy-of-clicks-company-203
title: 'entropy-of-clicks — Google case'
tags: [problemset, maths-stats-for-ml, information-theory, google]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Google'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Google** ranking and experimentation team might handle; it is not a real interview question or a claim that Google uses this exact task. The team needs a reliable implementation for traffic-distribution monitoring in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Compute Shannon entropy for a probability vector representing user-click outcomes.

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
[0.5, 0.5]
```

**Output**
```text
1.0
```

**Explanation:** Two equally likely outcomes contain one bit of uncertainty.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
</details>

## Theory

### The simple version

**entropy** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

H(P)=-\sum_i p_i\log_2 p_i.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Entropy measures uncertainty in a distribution; zero-probability events contribute zero by continuity.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(k) time and O(k) temporary space for filtering positive probabilities.
