---
name: research-shampoo-inverse-root
title: 'Shampoo: The Inverse Root'
tags: [research-papers, optimization, preconditioning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Shampoo scales the gradient by the inverse root of each preconditioner's eigenvalues. Raising eigenvalues to minus one over the root order gives the matrix power that Shampoo needs.

### From theory to code

Implement `inverse_root(eigs, power)`, the element-wise inverse root of positive eigenvalues.

### Constraints

- Work element-wise on the eigenvalues.

### Hints

<details>
<summary>Hint 1</summary>

Raise the eigenvalues to the power minus one over the root order.

</details>

## Theory

### The simple version

Larger curvature eigenvalues are damped more, which is the preconditioning effect; the root order sets how strongly.

### The formula

$$\lambda^{-1/p}$$

### How NumPy/PyTorch actually implements this

Shampoo applies this root to the eigenvalues of each preconditioner, obtained from an eigendecomposition.

## Explanation

Hand case: 16 to the minus one quarter is 1/2, and 81 to the minus one quarter is 1/3.
