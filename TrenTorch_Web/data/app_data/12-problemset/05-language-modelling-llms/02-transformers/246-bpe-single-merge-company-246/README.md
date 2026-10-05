---
name: bpe-single-merge-company-246
title: 'bpe-single-merge — Netflix case'
tags: [problemset, transformer-llm, tokenization-for-llms, netflix]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'Netflix'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
---

## Statement

Netflix-inspired text-ranking pipeline is building a compact subword vocabulary from frequent token pairs. You need to perform one BPE merge correctly so the vocabulary-building process can continue.

### Input Format

```python
solve(tokens, a, b, merged)
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
solve(["a","b","a"], 1, 1, ["a","b","a"])
```

**Output**

```text
["a","b","a"]
```

The output is produced by running the reference solution with these arguments.

**Example 2**

**Input**

```python
solve(["a","b","a"], 1, 1, ["a","b","a"])
```

**Output**

```text
["a","b","a"]
```

The output is produced by running the reference solution with these arguments.

### Hints

<details><summary>Hint</summary>

Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.

</details>

## Theory

### The simple version

**BPE** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

AB\rightarrow C when the selected pair AB occurs.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

BPE builds larger subword units by repeatedly merging frequent adjacent symbol pairs.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(n) time and O(n) output space.
