---
name: problem-161-teacher-forcing-step
title: 'Teacher Forcing Step'
tags: [problemset, sequence-models-attention, teacher-forcing]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'teacher forcing'
hint: 'target if use_target else predicted'
tools: [NumPy]
---

## Statement

Choose the input for the next decoder step. With teacher forcing (`use_target=True`) feed the ground-truth `target`; otherwise feed the model's own `predicted` output.

Implement `solve(target, predicted, use_target)`.

**Returns.** Return `target` if `use_target` is true, else `predicted` (the chosen object itself, not a copy).

### Examples

**Example 1**

Input:

```python
solve([1, 2, 3], [0, 1, 2], True)
```

Output:

```text
[1, 2, 3]
```

**Example 2**

Input:

```python
solve([1, 2, 3], [0, 1, 2], False)
```

Output:

```text
[0, 1, 2]
```

## Theory

### The simple version

While training a sequence generator you know the correct previous word. _Teacher forcing_ feeds that correct word to the next step instead of the model's own guess, which stops early mistakes from snowballing and makes training faster and more stable. The catch is _exposure bias_: at test time the model must use its own predictions, which it never practised on.

### The rule

$$\text{input}_{t+1}=\begin{cases}y_t&\text{teacher forcing}\\\hat y_t&\text{otherwise}\end{cases}$$

### Why it matters

- During training the correct previous word is known; feeding it instead of the model's own guess stops early mistakes from snowballing and makes training faster.
- The catch is exposure bias: at test time the model must use its own predictions, which it never practised on.

### How it works

1. If `use_target` is true, return the ground-truth token.
2. Otherwise return the model's own prediction.

### Worked example

With `use_target=True` the target $(1,2,3)$ is chosen over the prediction $(0,1,2)$, so the result is [1, 2, 3]. With `False` it would be $(0,1,2)$.

## Explanation

In practice a probability decides at each step whether to force (scheduled sampling): start near 1 and anneal toward 0 to reduce exposure bias.
