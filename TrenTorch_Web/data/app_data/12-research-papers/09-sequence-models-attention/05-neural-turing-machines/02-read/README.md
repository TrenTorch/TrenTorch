---
name: research-ntm-read
title: 'Neural Turing Machines: Reading the Memory'
tags: [research-papers, sequence-models, memory, neural-computation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A read in the NTM is a weighted sum of memory rows, so reading is differentiable and the controller learns where to look.

### From theory to code

Implement `ntm_read(w, memory)`, returning the weighted sum of memory rows.

### Constraints

- Weights sum to one.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the weight vector by the memory matrix.

</details>

## Theory

### The simple version

Reading all rows with soft weights is the NTM's way of making memory access a smooth operation that gradient descent can train.

### The formula

$$r = \sum_i w_i\,M_i$$

### How NumPy/PyTorch actually implements this

Memory-augmented controllers compute the read vector with one matrix product per step.

## Explanation

The read is the same weighted average used for attention contexts elsewhere in this track.
