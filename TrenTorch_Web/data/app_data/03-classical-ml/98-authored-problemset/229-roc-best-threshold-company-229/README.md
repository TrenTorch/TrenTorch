---
name: roc-best-threshold-company-229
title: "roc-best-threshold — Reddit case"
tags: [problemset, classical-ml, metrics-and-evaluation, reddit]
difficulty: Intermediate
kind: problemset
relatedModule: "part-classical-linear|Classification"
topic: "Classification"
caseCompany: "Reddit"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

Reddit-inspired moderation model produces continuous risk scores while the operations team needs a binary decision threshold. You need to evaluate candidate thresholds and select the one that maximizes Youden’s J statistic.

### Input Format

```python
solve(y, scores)
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

**ROC threshold** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

J(t)=TPR(t)-FPR(t).

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

A threshold is a decision policy layered on top of continuous scores; Youden's J balances sensitivity against false-positive rate.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

Sorting unique scores gives O(n log n); the simple implementation recomputes counts per threshold, O(n²).
