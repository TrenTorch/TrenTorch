---
name: research-ntk-linear-kernel
title: 'Neural Tangent Kernel: The Linear Kernel Matrix'
tags: [research-papers, classical-ml, kernels, ntk]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The neural tangent kernel (Jacot et al., 2018) says a very wide network trained by gradient descent behaves like a kernel method. The simplest kernel to start with is the linear one, a matrix of dot products between inputs.

### From theory to code

Implement `linear_kernel_matrix(X1, X2)`, returning the matrix of all pairwise dot products.

### Constraints

- The output has shape `(n1, n2)`.

### Hints

<details>
<summary>Hint 1</summary>

Multiply `X1` by the transpose of `X2`.

</details>

## Theory

### The simple version

Each entry measures how similar two inputs are, in the geometry the kernel defines. The NTK is built from such similarities, with the network's gradients as the features.

### The formula

$$K_{ij} = \langle x_i, x_j \rangle$$

### How NumPy/PyTorch actually implements this

`X1 @ X2.T` is the same computation; kernel libraries call it the linear kernel.

## Explanation

A Gram matrix of this form is symmetric and positive semidefinite, which the tests check.
