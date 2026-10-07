---
name: problem-147-train-validation-gap
title: 'Train/Validation Gap'
tags: [problemset, dl-training-theory, generalization]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'generalization'
hint: 'val_loss - train_loss'
tools: [NumPy]
---

## Statement

Compute the generalisation gap: validation loss minus training loss.

Implement `solve(train_loss, val_loss)`.

**Returns.** Return a float. A positive gap means the model does worse on validation data than on training data.

### Examples

**Example 1**

Input:

```python
solve(0.4, 0.6)
```

Output:

```text
0.2
```

**Example 2**

Input:

```python
solve(0.8, 0.7)
```

Output:

```text
-0.1
```

## Theory

### The simple version

The gap between training and validation loss is the quickest overfitting check. A model that fits the training data far better than unseen data has learned noise as well as signal. A large gap suggests more data, regularisation or a simpler model; a small gap with both losses high suggests underfitting.

### The formula

$$\text{gap}=L_{\text{val}}-L_{\text{train}}$$

## Explanation

In the first example validation is $0.2$ worse than training. The gap can be negative (second example), for instance when dropout is active during training but not during validation.
