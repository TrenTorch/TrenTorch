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
["l","o","w","l","o","w"],"l","o","lo"
```

**Output**
```text
["lo","w","lo","w"]
```

**Explanation:** Each non-overlapping l,o pair is replaced by the learned merged token.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
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
