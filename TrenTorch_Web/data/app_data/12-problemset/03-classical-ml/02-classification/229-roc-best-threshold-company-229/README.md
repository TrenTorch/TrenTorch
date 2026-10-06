---
name: roc-best-threshold-company-229
title: 'roc-best-threshold — Reddit case'
tags: [problemset, classical-ml, metrics-and-evaluation, reddit]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'Classification'
caseCompany: 'Reddit'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

Reddit-inspired moderation model produces continuous risk scores while the operations team needs a binary decision threshold. You need to evaluate candidate thresholds and select the one that maximizes Youden’s J statistic.

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
[1,1,0,0],[0.9,0.7,0.6,0.2]
```

**Output**
```text
0.7
```

**Explanation:** Threshold 0.7 predicts both positives and only one negative, giving a larger J than the other candidates.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
</details>

## Theory

### The simple version

**ROC threshold** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

J(t)=TPR(t)-FPR(t).

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

A threshold is a decision policy layered on top of continuous scores; Youden's J balances sensitivity against false-positive rate.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

Sorting unique scores gives O(n log n); the simple implementation recomputes counts per threshold, O(n²).
