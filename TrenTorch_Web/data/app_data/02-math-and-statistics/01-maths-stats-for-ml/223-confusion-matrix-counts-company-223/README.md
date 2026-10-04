---
name: confusion-matrix-counts-company-223
title: "confusion-matrix-counts — Salesforce case"
tags: [problemset, classical-ml, metrics-and-evaluation, salesforce]
difficulty: Beginner
kind: problemset
relatedModule: "part-data-foundations|Probability & Statistics"
topic: "Probability & Statistics"
caseCompany: "Salesforce"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

Salesforce-inspired model evaluation dashboard receives predicted and true binary labels from a validation run. You need to compute the confusion-matrix counts so the team can derive the metrics shown to model owners.

### Input Format

```python
solve(y, p)
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

**confusion matrix** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

TP=\sum 1[y=1,p=1],\;TN=\sum 1[y=0,p=0],\ldots

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

The confusion matrix decomposes classification outcomes so downstream metrics can be computed consistently.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(n) time and O(1) auxiliary space.
