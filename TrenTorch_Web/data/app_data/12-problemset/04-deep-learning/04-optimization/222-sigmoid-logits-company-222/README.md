---
name: sigmoid-logits-company-222
title: 'sigmoid-logits — ByteDance case'
tags: [problemset, classical-ml, logistic-regression, bytedance]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'ByteDance'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

ByteDance-inspired binary prediction service produces logits that must be converted into probabilities for downstream decision logic. You need to implement the sigmoid transformation correctly, including large positive and negative inputs.

### Input Format

```python
solve(z)
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
solve(1)
```

**Output**

```text
0.7310585786300049
```

The output is produced by running the reference solution with these arguments.

**Example 2**

**Input**

```python
solve(1)
```

**Output**

```text
0.7310585786300049
```

The output is produced by running the reference solution with these arguments.

### Hints

<details><summary>Hint</summary>

Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.

</details>

## Theory

### The simple version

**sigmoid** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

\sigma(z)=1/(1+e^{-z}).

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

A sigmoid converts a real log-odds value into a probability while the branch form keeps exponentials numerically safe.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(n) time and O(n) space.
