---
name: problem-199-rlhf-reward-normalization
title: 'RLHF Reward Normalization'
tags: [problemset, transformer-llm, rlhf-intuition]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'RLHF intuition'
hint: '(r - r.mean()) / r.std()'
tools: [NumPy]
---

## Statement

Normalise reward-model scores to zero mean and unit variance: subtract the mean and divide by the **population** standard deviation. The scores must not all be equal.

Implement `solve(rewards)`.

**Returns.** Return a float NumPy array. If every score is identical the standard deviation is $0$ and the result is not finite (`nan`).

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0])
```

Output:

```text
[-1.224745, 0.0, 1.224745]
```

**Example 2**

Input:

```python
solve([10.0, 20.0, 30.0, 40.0])
```

Output:

```text
[-1.341641, -0.447214, 0.447214, 1.341641]
```

## Theory

### The simple version

In RLHF a reward model scores the model's answers, but its raw scores can drift or have an arbitrary scale. Normalising each batch of rewards to mean 0 and spread 1 keeps the learning signal well-behaved: answers that are better than average get a positive reward, worse than average a negative one.

### The formula

$$\tilde r_i=\frac{r_i-\mu}{\sigma}$$

### Why it matters

- Reward-model scores can drift or have an arbitrary scale between batches.
- Normalising to zero mean and unit variance keeps the learning signal stable: better than average is positive, worse is negative.

### How it works

1. Subtract the mean.
2. Divide by the population standard deviation.

### Worked example

Rewards $(1,2,3)$ have mean $2$ and $\sigma=\sqrt{2/3}=0.8165$, so they become $(-1,0,1)/0.8165=[-1.224745, 0.0, 1.224745]$.

## Explanation

Shifting and scaling the rewards does not change which answer is best; it only changes how strongly the policy is pushed. The scale-free result is the same for $[1,2,3]$ and $[10,20,30]$.
