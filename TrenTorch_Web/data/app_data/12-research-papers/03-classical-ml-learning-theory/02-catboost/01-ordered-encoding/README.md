---
name: research-catboost-ordered-encoding
title: 'CatBoost: Ordered Target Encoding'
tags: [research-papers, classical-ml, boosting, catboost]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Target encoding replaces a category with the average label for that category. Done naively on the training set, each sample's own label leaks into its feature and the model overfits. CatBoost (Prokhorenkova et al., 2018) avoids this by encoding each sample using only the samples that came before it.

### From theory to code

Implement `ordered_target_encoding(cats, ys, prior, a)`, which encodes each sample from earlier samples in its category, blended with the prior.

### Constraints

- Process the samples in the given order.

### Hints

<details>
<summary>Hint 1</summary>

Keep a running sum and count per category. Encode the current sample first, then update the sums with its label.

</details>

## Theory

### The simple version

Ordering the samples means the statistic for sample `i` never includes `y_i`. The prior `a` keeps early encodings from being extreme when a category has few earlier samples.

### The formula

$$\hat x_i = \frac{\sum_{j < i,\ c_j = c_i} y_j + a\,p}{\#\{j < i : c_j = c_i\} + a}$$

### How NumPy/PyTorch actually implements this

CatBoost computes this encoding internally for categorical features, averaging over several random permutations.

## Explanation

The encoding of each sample uses only the prefix before it, which is the leakage-free property the paper relies on.
