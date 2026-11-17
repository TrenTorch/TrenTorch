---
name: research-deep-forest-cascade-predict
title: 'Deep Forest: Predicting From Averaged Forests'
tags: [research-papers, classical-ml, ensembles, deep-forest]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The last Deep Forest layer makes its prediction by averaging the class vectors of all its forests, then choosing the class with the largest average. This combines several forests' opinions into one answer.

### From theory to code

Implement `cascade_predict(forest_probas)`, which averages the forests' class vectors per sample and returns the argmax class.

### Constraints

- Ties are broken by the lowest class index.

### Hints

<details>
<summary>Hint 1</summary>

Stack the list into one array, average over the forest axis, then take `argmax` along the class axis.

</details>

## Theory

### The simple version

Averaging reduces the variance of individual forests. The argmax then turns the averaged probabilities into a single hard class.

### The formula

$$\hat y_i = \arg\max_c \frac{1}{K}\sum_{k=1}^{K} P^{(k)}_{i,c}$$

### How NumPy/PyTorch actually implements this

Ensemble classifiers in scikit-learn average `predict_proba` the same way before taking the class.

## Explanation

Here `K` is the number of forests in the final layer. NumPy's `argmax` already breaks ties toward the first index.
