---
name: problem-114-cross-entropy-from-logits
title: 'Cross-Entropy from Logits'
tags: [problemset, dl-core, loss-functions]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Loss Functions'
topic: 'loss functions'
hint: 'logsumexp(logits) - logits[target], with the max subtracted for stability'
tools: [NumPy]
---

## Statement

Compute the categorical cross-entropy loss of one example from its raw logits and the index of the true class, using the log-sum-exp trick for stability.

Implement `solve(logits, target)`.

**Returns.** Return a non-negative float: $\log\sum_j e^{z_j}-z_{\text{target}}$.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0], 2)
```

Output:

```text
0.407606
```

**Example 2**

Input:

```python
solve([5.0], 0)
```

Output:

```text
0.0
```

**Example 3**

Input:

```python
solve([1000.0, 0.0], 0)
```

Output:

```text
0.0
```

## Theory

### The simple version

Cross-entropy measures how surprised the model is by the true class. It equals the negative log of the probability the model assigned to that class, so confident correct answers cost almost nothing and confident wrong answers cost a lot.

### The formula

$$L=-\log\operatorname{softmax}(z)_t=\log\sum_j e^{z_j}-z_t$$

### Why it matters

- Cross-entropy is the standard classification loss: the negative log of the probability given to the true class.
- The logsumexp form is numerically safe.

### How it works

1. Compute $\operatorname{logsumexp}(z)$ with the max subtracted.
2. Subtract the target's logit.

### Worked example

For logits $(1,2,3)$: $\operatorname{logsumexp}=3+\ln(1+e^{-1}+e^{-2})=3.4076$. With target $2$ (logit $3$) the loss is $3.4076-3=0.407606$.

## Explanation

Computing softmax first and then the log can underflow. Writing the loss as $\operatorname{logsumexp}(z)-z_t$, with the maximum subtracted inside the sum, avoids that, so even logits of $1000$ are fine (third example, loss about $0$). A single-class problem has loss $0$ because the model is always right.
