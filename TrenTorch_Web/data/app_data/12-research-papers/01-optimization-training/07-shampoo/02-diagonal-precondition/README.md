---
name: research-shampoo-diagonal-precondition
title: 'Shampoo: Diagonal Preconditioning'
tags: [research-papers, optimization, preconditioning]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Shampoo takes the inverse fourth root of the preconditioners, not the inverse. With a left and right preconditioner each taking a quarter power, the overall scaling matches an inverse square root of the full curvature.

### From theory to code

Implement `precondition_diag(L, G, R)`, the two-sided scaling under diagonal preconditioners.

### Constraints

- Use the element-wise inverse fourth root of L and R.

### Hints

<details>
<summary>Hint 1</summary>

Multiply each row of G by L to the minus one quarter, and each column by R to the minus one quarter.

</details>

## Theory

### The simple version

Diagonal preconditioners make the two-sided update cheap to compute while keeping a per-row and per-column adaptive scale.

### The formula

$$\tilde G = L^{-1/4}\,G\,R^{-1/4}$$

### How NumPy/PyTorch actually implements this

Shampoo computes true matrix roots with an eigendecomposition; the diagonal case is the cheap special case.

## Explanation

Hand case: L[0] = 16 gives 0.5, R[1] = 16 gives 0.5, so entry [0,1] is 1 times 0.5 times 0.5 = 0.25.
