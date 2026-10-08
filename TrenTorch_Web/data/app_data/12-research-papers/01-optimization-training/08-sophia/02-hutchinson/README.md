---
name: research-sophia-hutchinson
title: 'Sophia: The Hutchinson Diagonal Estimate'
tags: [research-papers, optimization, second-order]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Sophia needs the Hessian diagonal, but forming the full Hessian is too costly. The Hutchinson estimator uses random +1 and -1 probes: multiplying a Hessian-vector product by the probe, element-wise, gives an unbiased diagonal estimate.

### From theory to code

Implement `hutchinson_estimate(Hu, u)`, the element-wise probe times the Hessian-vector product.

### Constraints

- The probe entries are plus or minus one.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the Hessian-vector product by the probe, element by element.

</details>

## Theory

### The simple version

Hessian-vector products cost about one extra backward pass, so the diagonal estimate is cheap enough to refresh every few steps.

### The formula

$$\hat h = u \odot (Hu),\qquad \mathbb E[u \odot Hu] = \operatorname{diag}(H)$$

### How NumPy/PyTorch actually implements this

The Monte Carlo test averages over many probes to recover the diagonal of a small matrix.

## Explanation

Hand case: probe [1, -1] times [2, 3] gives [2, -3].
