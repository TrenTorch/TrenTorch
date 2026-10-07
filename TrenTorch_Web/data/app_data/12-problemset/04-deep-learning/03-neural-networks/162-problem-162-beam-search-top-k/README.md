---
name: problem-162-beam-search-top-k
title: 'Beam Search Top-K'
tags: [problemset, sequence-models-attention, beam-search]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'beam search'
hint: 'start from the empty beam; expand every beam with every token; sort by (-score, tokens); keep k'
tools: [NumPy]
---

## Statement

Run beam search over precomputed per-step scores. `step_scores[t][v]` is the score (for example a log-probability) of choosing token `v` at step `t`, independent of earlier choices. Keep the `k` best partial sequences by cumulative score after each step; ties are broken in favour of the lexicographically smaller token sequence. `k` must be positive.

Implement `solve(step_scores, k)`.

**Returns.** Return a list of at most `k` tuples `(tokens, score)` sorted from best to worst, where `tokens` is a list of token ids.

### Examples

**Example 1**

Input:

```python
solve([[0.0, -1.0], [-2.0, 0.0]], 2)
```

Output:

```text
[([0, 1], 0.0), ([1, 1], -1.0)]
```

**Example 2**

Input:

```python
solve([[-1.0, 0.5, 0.0]], 1)
```

Output:

```text
[([1], 0.5)]
```

## Theory

### The simple version

Greedy decoding picks the single best word at each step and can paint itself into a corner. Beam search keeps the $k$ most promising partial sentences at every step, expands each of them with every possible next word, and prunes back to the best $k$. It explores more than greedy decoding at a fraction of the cost of exhaustive search.

### The recurrence

Beam$_t$ = top-$k$ of $\{(s\!\cdot\!v,\;\text{score}(s)+\text{step}_t[v])\;:\;s\in\text{Beam}_{t-1}\}$

## Explanation

Scores are added because they are log-probabilities, and adding logs multiplies probabilities. In the first example the best sequence takes token 0 then token 1 for a total of $0$, and the runner-up has score $-1$. The deterministic tie-break makes the output independent of dictionary or sort stability. Real decoders recompute the step scores from the model for each beam; here they are given.
