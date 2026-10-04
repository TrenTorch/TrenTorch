---
name: masked-sequence-mean-company-218
title: "masked-sequence-mean — Flipkart case"
tags: [problemset, sequence-models-attention, sequence-padding-and-masking, flipkart]
difficulty: Beginner
kind: problemset
relatedModule: "part-data-foundations|Probability & Statistics"
topic: "Probability & Statistics"
caseCompany: "Flipkart"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

Flipkart-inspired sequence model receives padded item histories where padding positions must not influence the representation. You need to compute the mean over only the unmasked positions so downstream ranking features are not biased by padding.

### Input Format

```python
solve(X, mask)
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

**masking** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

\bar{x}=\frac{\sum_i m_i x_i}{\sum_i m_i}.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Padding should not contribute semantic content to pooled sequence representations.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(nd) time for n tokens of dimension d.
