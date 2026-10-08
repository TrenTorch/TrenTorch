---
name: research-deep-forest-class-distribution
title: 'Deep Forest: The Class Vector'
tags: [research-papers, classical-ml, ensembles, deep-forest]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Deep Forest (Zhou & Feng, 2017) stacks layers of random forests, and each layer passes a class vector to the next one. The class vector is the distribution of labels in the leaves a sample reaches, averaged over trees.

### From theory to code

Implement `class_distribution(labels, n_classes)`, returning the fraction of samples in each class.

### Constraints

- Classes not present get a value of zero.

### Hints

<details>
<summary>Hint 1</summary>

Count with `np.bincount` using `minlength=n_classes`, then divide by the total.

</details>

## Theory

### The simple version

The class vector turns hard leaf votes into a soft estimate of class probability, which carries more information into the next layer.

### The formula

$$\hat p_c = \frac{1}{n}\sum_{i=1}^{n}\mathbb{1}[y_i = c]$$

### How NumPy/PyTorch actually implements this

The same counts are what `predict_proba` of a scikit-learn random forest averages over its trees.

## Explanation

This is an empirical class frequency; averaging these vectors across the trees of a forest gives the layer's output.
