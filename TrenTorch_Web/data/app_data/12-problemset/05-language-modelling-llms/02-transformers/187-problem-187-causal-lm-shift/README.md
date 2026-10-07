---
name: problem-187-causal-lm-shift
title: 'Causal LM Shift'
tags: [problemset, transformer-llm, pretraining-objectives]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'pretraining objectives'
hint: 'inputs = ids[:-1], targets = ids[1:]'
tools: [NumPy]
---

## Statement

Prepare next-token-prediction data from a sequence of token ids: the inputs are all tokens but the last, and the targets are all tokens but the first, so the model reads token $t$ and must predict token $t+1$.

Implement `solve(ids)`.

**Returns.** Return a tuple `(inputs, targets)` of NumPy arrays, each one shorter than `ids`.

### Examples

**Example 1**

Input:

```python
solve([10, 11, 12, 13])
```

Output:

```text
([10, 11, 12], [11, 12, 13])
```

**Example 2**

Input:

```python
solve([7, 8])
```

Output:

```text
([7], [8])
```

## Theory

### The simple version

A causal language model learns by predicting the next word. For every position, the input is the word there and the label is the following word, so one sentence provides many training examples at once, which is why the labels are just the inputs shifted by one.

### The shift

$$x_t=\text{ids}_t,\qquad y_t=\text{ids}_{t+1},\qquad t=0,\dots,T-2$$

## Explanation

Input `[10, 11, 12]` is paired with target `[11, 12, 13]`: reading 10 should predict 11, reading 11 should predict 12, and so on. The last token has no successor so it is never an input.
