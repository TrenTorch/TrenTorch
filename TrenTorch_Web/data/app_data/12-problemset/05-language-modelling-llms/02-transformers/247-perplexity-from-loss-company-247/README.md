---
name: perplexity-from-loss-company-247
title: 'perplexity-from-loss — Microsoft case'
tags: [problemset, transformer-llm, llm-evaluation, microsoft]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'Microsoft'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
---

## Statement

Microsoft-inspired language-model evaluation service reports perplexity from the average token loss. You need to convert the supplied loss into perplexity accurately so model runs can be compared on the same scale.

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
2.0
```

**Output**
```text
7.3890561
```

**Explanation:** Perplexity is the exponential of mean natural-log loss.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
</details>

## Theory

### The simple version

**perplexity** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

PPL=e^{\frac1N\sum_i -\log p_i}.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Perplexity expresses average uncertainty on the same multiplicative scale as the effective number of equally likely choices.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(1) time and space.
