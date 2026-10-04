---
name: binary-cross-entropy-company-236
title: "binary-cross-entropy — Mistral case"
tags: [problemset, dl-core, loss-functions, mistral]
difficulty: Intermediate
kind: problemset
relatedModule: "part-data-foundations|Probability & Statistics"
topic: "Probability & Statistics"
caseCompany: "Mistral"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

Mistral-inspired language-model evaluation component needs a stable binary cross-entropy calculation for a training diagnostic. You need to compute the loss from logits without introducing numerical overflow at extreme values.

### Input Format

```python
solve(z, y)
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

**BCE logits** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

\ell(z,y)=\max(z,0)-zy+\log(1+e^{-|z|}).

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Computing BCE from probabilities can underflow near extreme logits; the logits form avoids explicitly forming unstable probabilities.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(n) time and O(n) temporary space.
