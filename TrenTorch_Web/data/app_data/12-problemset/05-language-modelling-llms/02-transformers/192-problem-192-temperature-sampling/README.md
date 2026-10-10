---
name: problem-192-temperature-sampling
title: 'Temperature Sampling'
tags: [problemset, transformer-llm, generation]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'generation'
hint: 'softmax(logits / temperature) with the max subtracted'
tools: [NumPy]
---

## Statement

Compute the sampling distribution for temperature sampling: $\operatorname{softmax}(\text{logits}/T)$ for a positive temperature $T$, computed stably.

Implement `solve(logits,temperature)`.

**Returns.** Return a NumPy vector of probabilities that sums to 1.

### Examples

**Example 1**

Input:

```python
solve([2.0, 1.0, 0.0], 1.0)
```

Output:

```text
[0.665241, 0.244728, 0.090031]
```

**Example 2**

Input:

```python
solve([2.0, 1.0, 0.0], 0.1)
```

Output:

```text
[0.999955, 4.5e-05, 2.06106e-09]
```

**Example 3**

Input:

```python
solve([2.0, 1.0, 0.0], 10.0)
```

Output:

```text
[0.367165, 0.332225, 0.30061]
```

## Theory

### The simple version

The temperature is a dial between confident and adventurous text. Dividing the logits by a small $T$ exaggerates their differences, so the top word gets almost all the probability. A large $T$ shrinks the differences and makes the distribution flatter, so unlikely words get a real chance.

### The formula

$$p_i=\frac{e^{z_i/T}}{\sum_je^{z_j/T}}$$

### Why it matters

- Temperature is a dial between confident and adventurous text.
- Small temperatures sharpen the distribution and large ones flatten it.

### How it works

1. Divide the logits by the temperature.
2. Subtract the maximum and exponentiate.
3. Normalise.

### Worked example

At $T=1$ the logits $(2,1,0)$ give the model's own distribution, [0.665241, 0.244728, 0.090031]. At $T=0.1$ the logits become $(20,10,0)$ and almost all the probability goes to the first token.

## Explanation

$T=1$ is the model's own distribution; $T\to0$ approaches greedy decoding (second example, nearly all mass on the first token); $T\to\infty$ approaches the uniform distribution (third example). The maximum is subtracted for numerical stability. Note that this function returns the _distribution_, not a sampled token.
