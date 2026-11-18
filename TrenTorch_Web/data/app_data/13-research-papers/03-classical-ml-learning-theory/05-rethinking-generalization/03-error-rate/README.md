---
name: research-generalization-error-rate
title: 'Rethinking Generalization: The Error Rate'
tags: [research-papers, classical-ml, learning-theory, generalization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Generalization experiments measure errors on the training labels and on held-out labels. The error rate is the simplest measure: the fraction of predictions that disagree with the label.

### From theory to code

Implement `error_rate(pred, y)`, returning the fraction of mismatched predictions.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Compare the arrays elementwise, average the boolean mismatches.

</details>

## Theory

### The simple version

Error is one minus accuracy. The paper reports training error and test error on the same scale, so the two numbers can be compared directly.

### The formula

$$\text{err} = \frac{1}{n}\sum_{i=1}^{n}\mathbb{1}[\hat y_i \neq y_i]$$

### How NumPy/PyTorch actually implements this

`sklearn.metrics.zero_one_loss` returns this same quantity.

## Explanation

Averaging a boolean array gives the fraction of `True` values, which is the mismatch rate.
