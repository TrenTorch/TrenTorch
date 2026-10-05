---
name: research-ntk-kernel-ridge
title: 'Neural Tangent Kernel: Kernel Ridge Prediction'
tags: [research-papers, classical-ml, kernels, ntk]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Kernel ridge regression fits a function as a weighted sum of kernel values at the training points. In the NTK view, this is the function a wide network ends up learning under gradient descent.

### From theory to code

Implement `kernel_ridge_predict(K_train, y, K_test, lam)`, which solves `(K + lam I) alpha = y` and predicts with `K_test alpha`.

### Constraints

- Use `np.linalg.solve`, not an explicit inverse.

### Hints

<details>
<summary>Hint 1</summary>

Build `K_train + lam * I`, solve for the coefficients `alpha`, then multiply the test kernel by them.

</details>

## Theory

### The simple version

The ridge term keeps the system well-conditioned. Without it, a kernel matrix with near-zero eigenvalues would give unstable coefficients.

### The formula

$$\alpha = (K + \lambda I)^{-1} y, \qquad \hat f(x) = \sum_i \alpha_i\,k(x, x_i)$$

### How NumPy/PyTorch actually implements this

`sklearn.kernel_ridge.KernelRidge` uses the same linear solve on the kernel matrix.

## Explanation

The solve is a single linear system; for n training points it costs O(n^3), which is why kernel methods scale poorly with data.
