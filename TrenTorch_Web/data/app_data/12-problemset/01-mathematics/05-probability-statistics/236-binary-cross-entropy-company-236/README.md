---
name: binary-cross-entropy-company-236
title: 'binary-cross-entropy — Mistral case'
tags: [problemset, dl-core, loss-functions, mistral]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Mistral'
hint: 'mean of max(z,0) - z*y + log1p(exp(-|z|))'
tools: [NumPy]
---

## Statement

Mistral-inspired language-model evaluation component needs a stable binary cross-entropy calculation for a training diagnostic. You need to compute the loss from logits without introducing numerical overflow at extreme values.

Compute the mean binary cross-entropy from logits `z` and 0/1 labels `y` with a form that never overflows: $\max(z,0)-zy+\log(1+e^{-|z|})$ averaged over the samples.

Implement `solve(z,y)`.

**Returns.** Return a non-negative Python float.

Compute the mean binary cross-entropy from logits `z` and 0/1 labels `y` with a form that never overflows: $\max(z,0)-zy+\log(1+e^{-|z|})$ averaged over the samples.

Implement `solve(z,y)`.

**Returns.** Return a non-negative Python float.

### Examples

**Example 1**

Input:

```python
solve([0.0, 2.0], [0, 1])
```

Output:

```text
0.410038
```

**Example 2**

Input:

```python
solve([1000.0, -1000.0], [1, 0])
```

Output:

```text
0.0
```

**Example 3**

Input:

```python
solve([1000.0], [0])
```

Output:

```text
1000.0
```

## Theory

### The simple version

Binary cross-entropy punishes confident wrong predictions very hard and barely penalises confident right ones. Computing it by first applying the sigmoid breaks down for extreme logits, because the sigmoid rounds to exactly $0$ or $1$ and $\log0=-\infty$. The logit form avoids that.

### The stable form

$$\ell(z,y)=\max(z,0)-zy+\log\!\big(1+e^{-|z|}\big)$$

### Why it matters

- Binary cross-entropy punishes confident wrong predictions very hard and is the standard loss for yes/no models.
- The logit form never takes the log of a probability that has rounded to $0$ or $1$.

### How it works

1. For each sample compute $\max(z,0)-zy+\log(1+e^{-|z|})$.
2. Average over samples.

### Worked example

Logit $0$ with label $0$ costs $\log2=0.6931$ (the model is unsure). Logit $2$ with label $1$ costs $2-2+\log(1+e^{-2})=0.1269$ (confident and right). The mean is 0.410038.

## Explanation

Only $e^{-|z|}\le1$ is ever evaluated, so there is no overflow, and `log1p` keeps precision for tiny arguments. In the first example the zero logit costs $\log2\approx0.693$ and the confident correct logit $2$ costs about $0.127$. A confidently _wrong_ logit of $1000$ (third example) costs about $1000$.
