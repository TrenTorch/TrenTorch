---
name: beam-search-step-company-244
title: 'beam-search-step — Zoom case'
tags: [problemset, sequence-models-attention, beam-search-decoding, zoom]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'Zoom'
hint: 'expand each beam with every token, sort by (-score, tokens), keep width'
tools: [NumPy]
---

## Statement

Zoom-inspired speech/transcription prototype keeps several candidate sequences instead of committing to a single next token. You need to perform one beam-search expansion and retain the highest-scoring candidates deterministically.

Perform one beam-search expansion step. `beams` is a list of `(tokens, score)` pairs (`tokens` is a list), `next_logp` holds the log-probability of every vocabulary token for the next position (the same for every beam) and `width` is the number of beams to keep. Extend every beam with every token, add the log-probability to the score, and keep the `width` best candidates; ties are broken in favour of the lexicographically smaller token list.

Implement `solve(beams,next_logp,width)`.

**Returns.** Return a list of at most `width` `(tokens, score)` pairs sorted from best to worst.

### Examples

**Example 1**

Input:

```python
solve([([], 0.0)], [-0.1, -2.0, -1.0], 2)
```

Output:

```text
[([0], -0.1), ([2], -1.0)]
```

**Example 2**

Input:

```python
solve([([1], -0.5), ([2], -0.7)], [-0.2, -0.9], 3)
```

Output:

```text
[([1, 0], -0.7), ([2, 0], -0.9), ([1, 1], -1.4)]
```

## Theory

### The simple version

Beam search keeps several candidate sequences alive instead of committing to the single most likely next word. Each step extends every candidate with every possible next token, scores the extended sequences, and prunes back to the best few. It finds higher-probability sequences than greedy decoding for a modest cost.

### One step

$$\text{Beams}'=\operatorname{top}_w\{(s\cdot v,\;\text{score}(s)+\log p(v\mid s))\}$$

## Explanation

Scores are sums of log-probabilities, i.e. logs of products of probabilities, so higher (closer to zero) is better. In the first example the best two continuations of the empty sequence are token 0 (score $-0.1$) and token 2 ($-1.0$). Sorting on `(-score, tokens)` makes the output order fully deterministic.
