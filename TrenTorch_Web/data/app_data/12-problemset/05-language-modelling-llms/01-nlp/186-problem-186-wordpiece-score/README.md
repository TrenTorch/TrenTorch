---
name: problem-186-wordpiece-score
title: 'WordPiece Score'
tags: [problemset, transformer-llm, tokenization]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|NLP'
topic: 'tokenization'
hint: 'pair_count / (left_count * right_count)'
tools: [NumPy]
---

## Statement

Compute the WordPiece merge score of a candidate pair: the pair's frequency divided by the product of the frequencies of its two parts, $\dfrac{\text{count}(ab)}{\text{count}(a)\cdot\text{count}(b)}$.

Implement `solve(pair_count,left_count,right_count)`.

**Returns.** Return a float. The part frequencies must be positive.

### Examples

**Example 1**

Input:

```python
solve(2.0, 3.0, 1.0)
```

Output:

```text
0.666667
```

**Example 2**

Input:

```python
solve(5.0, 5.0, 5.0)
```

Output:

```text
0.2
```

## Theory

### The simple version

BPE merges the most _frequent_ pair, which tends to merge common but unrelated pieces like "of" and "the". WordPiece instead asks how much more often the two pieces appear together than you would expect if they were independent. A high score means the parts belong together.

### The formula

$$\text{score}(a,b)=\frac{\text{count}(ab)}{\text{count}(a)\,\text{count}(b)}$$

### Why it matters

- BPE merges the most frequent pair, which often glues common but unrelated pieces together.
- WordPiece compares how often the pair occurs with how often you would expect it by chance, so pieces that truly belong together score high.

### How it works

1. Multiply the counts of the two parts.
2. Divide the pair's count by that product.

### Worked example

Pair count $2$, left part $3$, right part $1$: $2/(3\cdot1)=0.666667$. A pair of two very common parts would score lower for the same pair count.

## Explanation

Dividing by the product of the individual counts penalises pairs made of very common parts. In the first example $2/(3\cdot1)=0.667$; in the second a pair made of two frequent pieces scores only $0.2$.
