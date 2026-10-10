---
name: problem-190-top-k-sampling
title: 'Top-K Sampling'
tags: [problemset, transformer-llm, generation]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'generation'
hint: 'keep the k largest logits, softmax, then rng.choice(len(logits), p=p)'
tools: [NumPy]
---

## Statement

Sample the next token using top-$k$ sampling. Keep only the `k` largest logits, set all others to a very large negative value, turn the result into probabilities with a softmax and draw one token with `rng.choice(len(logits), p=p)` where `rng` is a `numpy.random.Generator`.

Implement `solve(logits, k, rng)`.

**Returns.** Return the sampled token index (an integer in `0 .. len(logits)-1`). With `k=1` the largest logit is always returned.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0], 1, np.random.default_rng(0))
```

Output:

```text
2
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0], 2, np.random.default_rng(0))
```

Output:

```text
3
```

## Theory

### The simple version

Always picking the most likely word gives dull, repetitive text, but sampling from the full distribution sometimes picks absurd low-probability words. Top-$k$ sampling compromises: throw away everything outside the $k$ most likely words, renormalise, and sample from those.

### The procedure

1. Keep the $k$ largest logits.
2. $p=\operatorname{softmax}$ over the kept logits (the others get probability $0$).
3. Draw one index from $p$.

### Why it matters

- Always taking the most likely word gives dull, repetitive text, while sampling from everything sometimes picks absurd rare words.
- Top-$k$ sampling keeps only the $k$ best candidates and samples among them.

### How it works

1. Keep the $k$ largest logits and set the others to $-10^9$.
2. Softmax.
3. Draw one index with the generator.

### Worked example

With $k=1$ only the largest logit $3$ (index $2$) survives, so it gets probability $1$ and the sample is always 2.

## Explanation

The excluded logits are replaced by $-10^9$ so their softmax weight is zero. `k=1` reduces to greedy decoding. The draw is random, so only a seeded generator makes the result reproducible.
