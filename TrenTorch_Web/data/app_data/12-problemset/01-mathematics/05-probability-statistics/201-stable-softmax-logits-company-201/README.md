---
name: stable-softmax-logits-company-201
title: 'stable-softmax-logits — Netflix case'
tags: [problemset, maths-stats-for-ml, probability-foundations, netflix]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Netflix'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Netflix** ranking and experimentation team might handle; it is not a real interview question or a claim that Netflix uses this exact task. The team needs a reliable implementation for score-to-probability conversion in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Given a vector of model logits, convert them into probabilities without overflowing when logits are large.

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
[1000.0, 1001.0]
```

**Output**

```text
[0.26894142, 0.73105858]
```

**Explanation:** Subtracting the maximum logit preserves the softmax ratios while keeping exponentials numerically bounded.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
</details>

## Theory

### The simple version

**stable softmax** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

p_i=\frac{e^{z_i}}{\sum_j e^{z_j}}; replacing z_i by z_i-c for every i leaves p_i unchanged.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

softmax converts arbitrary scores into a probability distribution while preserving relative preference between logits.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(n) time and O(n) space; the maximum-shift is essential for numerical stability.
