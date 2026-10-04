---
name: entropy-of-clicks-company-203
title: "entropy-of-clicks — Google case"
tags: [problemset, maths-stats-for-ml, information-theory, google]
difficulty: Beginner
kind: problemset
relatedModule: "part-data-foundations|Probability & Statistics"
topic: "Probability & Statistics"
caseCompany: "Google"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Google** ranking and experimentation team might handle; it is not a real interview question or a claim that Google uses this exact task. The team needs a reliable implementation for traffic-distribution monitoring in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Compute Shannon entropy for a probability vector representing user-click outcomes.

### Input Format

```python
solve(p)
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
-0.0
```

The output is produced by running the reference solution with these arguments.

**Example 2**

**Input**
```python
solve(1)
```

**Output**
```text
-0.0
```

The output is produced by running the reference solution with these arguments.

### Hints

<details><summary>Hint</summary>

Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.

</details>

## Theory

### The simple version

**entropy** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

H(P)=-\sum_i p_i\log_2 p_i.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Entropy measures uncertainty in a distribution; zero-probability events contribute zero by continuity.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(k) time and O(k) temporary space for filtering positive probabilities.
