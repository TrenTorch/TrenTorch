---
name: problem-191-top-p-sampling
title: 'Top-P Sampling'
tags: [problemset, transformer-llm, generation]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'generation'
hint: 'softmax, sort descending, cumsum, keep the prefix that reaches p_cut, renormalise, rng.choice'
tools: [NumPy]
---

## Statement

Sample the next token with top-$p$ (nucleus) sampling. Turn the logits into probabilities with a softmax, sort them from largest to smallest, keep every token whose cumulative probability is at most `p_cut` **plus** the first token that pushes the total past `p_cut`, renormalise those probabilities and draw one index with `rng.choice(len(logits), p=q)` where `rng` is a `numpy.random.Generator`.

Implement `solve(logits, p_cut, rng)`.

**Returns.** Return the sampled token index (an integer). With a small `p_cut` only the most likely token survives.

### Examples

**Example 1**

Input:

```python
solve([2.0, 1.0, 0.0], 0.5, np.random.default_rng(0))
```

Output:

```text
0
```

**Example 2**

Input:

```python
solve([0.0, 0.0, 0.0, 0.0], 1.0, np.random.default_rng(1))
```

Output:

```text
2
```

## Theory

### The simple version

Top-$k$ always keeps the same number of candidates, even when the model is very sure (then $k$ is too generous) or very unsure (then $k$ is too strict). Top-$p$ adapts: keep the smallest group of most likely words whose probabilities add up to $p$, and sample only from them.

### The procedure

1. $\pi=\operatorname{softmax}(\text{logits})$, sorted in decreasing order.
2. Keep the shortest prefix whose cumulative sum reaches $p$.
3. Renormalise and sample.

## Explanation

When the model is confident, the nucleus is a single token or two; when it is uncertain, the nucleus is wide. The token that crosses the threshold is always included, so the kept set is never empty. In the second example the four tokens are equally likely, and `p_cut=1` keeps all of them.
