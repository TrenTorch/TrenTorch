---
name: problem-198-in-context-majority-vote
title: 'In-Context Majority Vote'
tags: [problemset, transformer-llm, in-context-learning]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'in-context learning'
hint: 'np.unique with counts, then argmax'
tools: [NumPy]
---

## Statement

Predict a label by majority vote over the labels of the demonstrations in a prompt. If several labels tie, the smallest label wins.

Implement `solve(labels)`.

**Returns.** Return the winning label.

### Examples

**Example 1**

Input:

```python
solve([0, 1, 1, 0, 1])
```

Output:

```text
1
```

**Example 2**

Input:

```python
solve([2, 3, 3, 2])
```

Output:

```text
2
```

## Theory

### The simple version

In-context learning shows a language model a few labelled examples in its prompt and asks it to label a new one. A simple baseline ignores the new input and just predicts whatever label is most common among the demonstrations, which tells you how much of the model's accuracy comes from the label distribution alone.

### The rule

$$\hat y=\arg\max_c\#\{i:y_i=c\}$$

### Why it matters

- The majority label among the demonstrations is the baseline a few-shot method must beat.
- It shows how much of a model's accuracy comes from the label distribution alone.

### How it works

1. Count each label.
2. Return the most frequent (smallest on ties).

### Worked example

Labels $(0,1,1,0,1)$ contain two zeros and three ones, so the majority is 1.

## Explanation

Counting is done with `np.unique`, which returns the labels in sorted order, and `argmax` picks the first maximum, so ties resolve to the smaller label (second example returns 2). The majority-label baseline is the number any few-shot method must beat.
