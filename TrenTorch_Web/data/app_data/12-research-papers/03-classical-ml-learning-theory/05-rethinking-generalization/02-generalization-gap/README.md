---
name: research-generalization-gap
title: 'Rethinking Generalization: The Generalization Gap'
tags: [research-papers, classical-ml, learning-theory, generalization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The generalization gap is how much better a model does on data it trained on than on data it has not seen. The paper's point is that this gap can be near 100 percent for random labels, while staying small for real labels.

### From theory to code

Implement `generalization_gap(train_acc, test_acc)`, returning the training accuracy minus the test accuracy.

### Constraints

- Accuracies are between 0 and 1.

### Hints

<details>
<summary>Hint 1</summary>

Subtract the two numbers.

</details>

## Theory

### The simple version

A large gap means the model has memorized the training data rather than learned a rule that carries over. Tracking this difference is the simplest check for overfitting.

### The formula

$$\text{gap} = \text{acc}_{\text{train}} - \text{acc}_{\text{test}}$$

### How NumPy/PyTorch actually implements this

Training dashboards plot exactly this difference over epochs to show when overfitting starts.

## Explanation

The quantity is a difference of two empirical accuracies, computed on separate data.
