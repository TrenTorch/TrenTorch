---
name: stable-softmax-logits-company-201
title: "stable-softmax-logits — Netflix case"
tags: [problemset, maths-stats-for-ml, probability-foundations, netflix]
difficulty: Beginner
kind: problemset
relatedModule: "part-data-foundations|Probability & Statistics"
topic: "Probability & Statistics"
caseCompany: "Netflix"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Netflix** ranking and experimentation team might handle; it is not a real interview question or a claim that Netflix uses this exact task. The team needs a reliable implementation for score-to-probability conversion in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Given a vector of model logits, convert them into probabilities without overflowing when logits are large.

### Input Format

```python
solve(logits)
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

**stable softmax** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

p_i=\frac{e^{z_i}}{\sum_j e^{z_j}}; replacing z_i by z_i-c for every i leaves p_i unchanged.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

softmax converts arbitrary scores into a probability distribution while preserving relative preference between logits.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(n) time and O(n) space; the maximum-shift is essential for numerical stability.
