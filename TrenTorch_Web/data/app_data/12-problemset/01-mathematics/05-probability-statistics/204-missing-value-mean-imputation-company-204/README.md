---
name: missing-value-mean-imputation-company-204
title: 'missing-value-mean-imputation — Microsoft case'
tags: [problemset, data-stats-for-ds, data-cleaning, microsoft]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Microsoft'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Microsoft** ranking and experimentation team might handle; it is not a real interview question or a claim that Microsoft uses this exact task. The team needs a reliable implementation for feature cleaning in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Replace NaN entries in each feature column with that column's mean computed from the observed values.

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
[[1.0,nan],[3.0,5.0]]
```

**Output**

```text
[[1.0,5.0],[3.0,5.0]]
```

**Explanation:** The first column mean is two and the second column has no missing value, so only the missing entry is replaced.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
</details>

## Theory

### The simple version

**missing value imputation** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

m_j=\frac{1}{|O_j|}\sum_{i\in O_j}x_{ij}.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Mean imputation is a simple deterministic baseline; the key is computing each statistic only from observed values.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(nd) time and O(nd) space because the result is copied.
