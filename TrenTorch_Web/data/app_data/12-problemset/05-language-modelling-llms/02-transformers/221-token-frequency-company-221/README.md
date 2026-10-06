---
name: token-frequency-company-221
title: 'token-frequency — LinkedIn case'
tags: [problemset, transformer-llm, tokenization-for-llms, linkedin]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'LinkedIn'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
---

## Statement

LinkedIn-inspired text analytics service is building a lightweight vocabulary report from a batch of documents. You need to count token occurrences consistently so the team can identify the most frequent terms for the next modeling stage.

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
[2,1,2,3,2,1]
```

**Output**
```text
{1: 2, 2: 3, 3: 1}
```

**Explanation:** Token two occurs three times, token one twice, and token three once.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
</details>

## Theory

### The simple version

**token frequency** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

c(t)=\sum_i 1[x_i=t].

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Frequency counts are a simple building block for vocabulary statistics and data diagnostics.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(n) expected time and O(v) space for v distinct tokens.
