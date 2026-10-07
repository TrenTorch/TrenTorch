---
name: problem-163-length-normalized-beam-search
title: 'Length-Normalized Beam Search'
tags: [problemset, sequence-models-attention, beam-search]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'beam search'
hint: 'max by score / max(1,len)**alpha, lexicographically smaller tokens on ties'
tools: [NumPy]
---

## Statement

Pick the best finished beam by **length-normalised** score $\text{score}/\text{len}^{\alpha}$ (a length of 0 counts as 1). `beams` is a list of `(tokens, score)` pairs. Ties are broken in favour of the lexicographically smaller token list. `alpha` must be non-negative and `beams` must not be empty (otherwise `ValueError`).

Implement `solve(beams, alpha)`.

**Returns.** Return the winning `(tokens, score)` pair.

### Examples

**Example 1**

Input:

```python
solve([([1, 2], -3.0), ([3], -1.0)], 1.0)
```

Output:

```text
([3], -1.0)
```

**Example 2**

Input:

```python
solve([([1, 2, 3], -3.0), ([3], -2.0)], 1.0)
```

Output:

```text
([1, 2, 3], -3.0)
```

**Example 3**

Input:

```python
solve([([1, 2, 3], -3.0), ([3], -2.0)], 0.0)
```

Output:

```text
([3], -2.0)
```

## Theory

### The simple version

Summed log-probabilities are always negative and grow more negative with every extra token, so beam search is biased toward short outputs. Dividing by $\text{length}^{\alpha}$ removes (fully for $\alpha=1$, partially for smaller $\alpha$) that bias so long and short candidates compete fairly.

### The formula

$$\text{score}_{\text{norm}}=\frac{\log P(y)}{|y|^{\alpha}}$$

## Explanation

With $\alpha=0$ there is no normalisation and the raw score decides (third example picks the short beam with $-2$). With $\alpha=1$ the three-token beam has average score $-1$, which beats $-2$ for the one-token beam (second example).
