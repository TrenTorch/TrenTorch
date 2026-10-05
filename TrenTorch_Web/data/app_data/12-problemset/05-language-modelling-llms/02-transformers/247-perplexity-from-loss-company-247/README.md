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

```python
solve(mean_nll)
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
solve(1.0)
```

**Output**

```text
2.718281828459045
```

The output is produced by running the reference solution with these arguments.

**Example 2**

**Input**

```python
solve(1.0)
```

**Output**

```text
2.718281828459045
```

The output is produced by running the reference solution with these arguments.

### Hints

<details><summary>Hint</summary>

Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.

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
