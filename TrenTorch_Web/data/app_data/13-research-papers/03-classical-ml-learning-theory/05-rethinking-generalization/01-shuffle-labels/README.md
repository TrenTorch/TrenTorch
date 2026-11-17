---
name: research-generalization-shuffle-labels
title: 'Rethinking Generalization: Shuffling the Labels'
tags: [research-papers, classical-ml, learning-theory, generalization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Zhang et al. (2017) showed that neural networks can fit completely random labels perfectly, memorizing the training set. Shuffling the labels is the first step of that experiment: the labels keep their distribution but lose their connection to the inputs.

### From theory to code

Implement `shuffle_labels(y, rng)`, which returns a random permutation of the labels.

### Constraints

- Use the provided `rng`, so results are reproducible.

### Hints

<details>
<summary>Hint 1</summary>

Call `rng.permutation` on a NumPy copy of the labels.

</details>

## Theory

### The simple version

A model that generalizes should not be able to fit labels with no real pattern, so this test separates memorization from learning. The paper uses exactly this construction.

### The formula

$$\tilde y = \pi(y), \qquad \pi \text{ a uniformly random permutation of indices}$$

### How NumPy/PyTorch actually implements this

Experiments with randomized labels generate them with `np.random.Generator.permutation` in the same way.

## Explanation

The permutation preserves the label counts, so class balance is unchanged while the input-label relationship is destroyed.
