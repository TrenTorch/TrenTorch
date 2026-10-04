---
name: best-stump-threshold-company-209
title: "best-stump-threshold — Zomato case"
tags: [problemset, classical-ml-trees-ensembles, decision-trees, zomato]
difficulty: Beginner
kind: problemset
relatedModule: "part-data-foundations|Probability & Statistics"
topic: "Probability & Statistics"
caseCompany: "Zomato"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

Zomato-inspired ranking filter uses a single numeric feature to separate likely outcomes from unlikely ones. You need to find the threshold that gives the best classification score, providing a simple baseline before the team deploys a larger model.

### Input Format

```python
solve(x, y)
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

**decision stump** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

I(t)=\frac{n_L}{n}G_L+\frac{n_R}{n}G_R.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

A one-dimensional tree split only needs to consider boundaries between distinct sorted values; any threshold inside the same interval makes the same partition.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

Sorting costs O(n log n); evaluating candidate splits in this simple reference is O(n²) because each impurity is recomputed.
