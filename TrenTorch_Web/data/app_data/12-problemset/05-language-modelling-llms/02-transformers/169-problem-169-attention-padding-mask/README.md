---
name: problem-169-attention-padding-mask
title: 'Attention Padding Mask'
tags: [problemset, sequence-models-attention, sequence-padding]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'sequence padding'
hint: 'ids != pad_id'
tools: [NumPy]
---

## Statement

Build the padding mask for attention: given a row of token ids, mark every position that holds a real token (`True`) and every position equal to `pad_id` (`False`).

Implement `solve(ids, pad_id)`.

**Returns.** Return a boolean NumPy array of the same length as `ids`.

### Examples

**Example 1**

Input:

```python
solve([5, 6, 0, 0], 0)
```

Output:

```text
[True, True, False, False]
```

**Example 2**

Input:

```python
solve([[3, 0], [4, 5]], 0)
```

Output:

```text
[[True, False], [True, True]]
```

## Theory

### The simple version

Sentences in a batch have different lengths, so the short ones are padded with a dummy token. Attention must ignore those dummy positions, otherwise the model would attend to meaningless padding. The padding mask says which keys are real.

### The definition

$$\text{mask}_j=\mathbb 1[\,\text{id}_j\ne\text{pad\_id}\,]$$

### Why it matters

- Sentences in a batch have different lengths, so short ones are padded with a dummy token.
- Attention must ignore those dummy positions or it would attend to meaningless padding.

### How it works

1. Compare every token id with the padding id.
2. `True` where they differ (a real token).

### Worked example

For $(5,6,0,0)$ with padding id $0$ the first two positions are real tokens and the last two are padding, so the mask is [True, True, False, False].

## Explanation

The comparison works on arrays of any shape (the second example masks a batch of two sequences). The `False` positions are later given a very negative score so the softmax assigns them zero weight. A genuine token whose id happens to equal `pad_id` would be masked too, so the padding id must be reserved.
