---
name: research-zeiler-max-switches
title: 'Visualizing Convolutional Networks: Max-pooling Switches'
tags: [research-papers, computer-vision, cnn, interpretability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

To see what a max-pooling layer discards, Zeiler and Fergus recorded the position of each pooled maximum, its switch. Those switches let a deconvolution network place activations back where they came from.

### From theory to code

Implement `max_pool_switches(x, size)`, returning the offset of the maximum within each pooling window.

### Constraints

- Work on a 1D signal for simplicity.

### Hints

<details>
<summary>Hint 1</summary>

Reshape the signal into rows of length `size`, then take the argmax of each row.

</details>

## Theory

### The simple version

The switches are the information max-pooling throws away, and recording them makes the pooling step invertible in part. Visualization then shows which input pixels produced each activation.

### The formula

$$s_j = \arg\max_{i \in \text{window}_j} x_i$$

### How NumPy/PyTorch actually implements this

Deconvnet visualizers store exactly these indices from `F.max_pool2d(..., return_indices=True)`.

## Explanation

Ties go to the first position, matching NumPy's argmax and the paper's convention.
