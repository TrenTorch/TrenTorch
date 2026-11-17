---
name: problem-188-masked-lm-labels
title: 'Masked LM Labels'
tags: [problemset, transformer-llm, pretraining-objectives]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'pretraining objectives'
hint: 'labels = full(ignore_index); labels[mask] = ids[mask]'
tools: [NumPy]
---

## Statement

Create the labels for masked-language-model training. `mask` marks the positions that were selected for prediction. The labels equal the original token id at selected positions and `ignore_index` (default $-100$) everywhere else, so the loss only counts the masked positions. The token ids themselves are returned unchanged.

Implement `solve(ids, mask, ignore_index=-100)`.

**Returns.** Return a tuple `(ids, labels)` of integer NumPy arrays; `ids` is a copy of the input.

### Examples

**Example 1**

Input:

```python
solve([5, 6, 7, 8], [False, True, False, True])
```

Output:

```text
([5, 6, 7, 8], [-100, 6, -100, 8])
```

**Example 2**

Input:

```python
solve([5, 6], [False, False], ignore_index=-1)
```

Output:

```text
([5, 6], [-1, -1])
```

## Theory

### The simple version

BERT-style models learn by guessing words that have been hidden. Only the hidden positions should be graded; the others are ignored by giving them a label the loss function skips (conventionally $-100$ in PyTorch's cross-entropy).

### The labels

$$\text{label}_t=\begin{cases}\text{id}_t&t\text{ masked}\\\text{ignore\_index}&\text{otherwise}\end{cases}$$

### Why it matters

- BERT-style training grades only the hidden positions.
- The ignore label tells the loss to skip the others.

### How it works

1. Fill labels with the ignore value.
2. Copy the true ids at masked positions.

### Worked example

Positions $1$ and $3$ are masked, so the labels are $(-100,6,-100,8)$: ([5, 6, 7, 8], [-100, 6, -100, 8]).

## Explanation

Replacing the selected input tokens by a `[MASK]` token is a separate step and is not done here. If nothing is masked, every label is the ignore value (second example), so the loss has nothing to learn from that sequence.
