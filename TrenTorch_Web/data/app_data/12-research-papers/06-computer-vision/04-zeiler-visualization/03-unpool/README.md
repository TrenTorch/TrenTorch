---
name: research-zeiler-unpool
title: 'Visualizing Convolutional Networks: Unpooling With Switches'
tags: [research-papers, computer-vision, cnn, interpretability]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Unpooling with switches puts each activation back at the position where its maximum came from, and leaves zeros elsewhere. The visualizer then runs the network backwards to project a feature onto image pixels.

### From theory to code

Implement `unpool_with_switches(pooled, switches, size)`, the inverse of max-pooling on the recorded maxima.

### Constraints

- Zeros fill all non-switch positions.

### Hints

<details>
<summary>Hint 1</summary>

Allocate zeros of length `len(pooled) * size`, then write each pooled value at window start plus its switch offset.

</details>

## Theory

### The simple version

Unpooling is not a true inverse, since the non-maximal values are lost, but placing maxima back in their positions shows which pixels a unit responded to.

### The formula

$$y_{j\cdot s + s_j} = p_j, \qquad y_i = 0 \text{ otherwise}$$

### How NumPy/PyTorch actually implements this

The deconvnet visualizer uses `F.max_unpool2d` with the stored indices to do this.

## Explanation

The fancy indexing writes every window's maximum in one vectorized assignment.
