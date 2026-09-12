---
name: math-eigenvalues-eigenvectors
title: Eigenvalues and eigenvectors of a small matrix
tags: [linear-algebra, matrices]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Apply a matrix to a vector and, in general, you get a vector pointing in some new direction, rotated and rescaled both. But every matrix has special directions where nothing rotates: feed it a vector already pointing that way, and you get back the same direction, only longer or shorter. Those special, rotation-immune directions are eigenvectors, and how much they stretch is the eigenvalue.

Why bother finding them? Because they tell you what a matrix _actually does_ to space, stripped of the confusing mix of rotation and scaling every other direction shows. A covariance matrix's eigenvectors, for instance, point along the directions your data varies the most and the least, exactly what PCA (a later question) exploits to compress data without losing much information.

### From theory to code

Theory restricts to real symmetric matrices specifically, where eigenvalues are guaranteed real and a specialized, numerically stable routine exists. Implement the decomposition using that routine, and a separate check that verifies the defining equation directly for any claimed eigenvalue/eigenvector pair.

Implement `eigen_decomposition(a)` and `verify_eigenpair(a, eigenvalue, eigenvector)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `a` is always real and symmetric (`a == a.T`).
- Use the specialized symmetric-matrix routine, not the general-purpose one, Theory explains why they differ.
- `verify_eigenpair` checks the actual defining equation, not just that `v` "looks like" an eigenvector.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

NumPy has two different eigen-decomposition functions, one general, one specifically for symmetric/Hermitian matrices. The specialized one is faster, more stable, and always returns real values, exactly what this question wants.

</details>

<details>
<summary>Hint 2</summary>

The defining equation is `A @ v = lambda * v`. Compute both sides and compare them, that's the whole check.

</details>

## Theory

### The simple version

Push on a wheel at a random spot and it both spins and translates. Push exactly through its center and it only translates, no spin. Matrices act on vectors the same way: most directions get rotated and scaled together, but a few special directions, the eigenvectors, only ever get scaled, never rotated off their own line.

### The formula

An **eigenvector** of a square matrix `A` is a nonzero vector `v` that `A` only stretches or shrinks, never rotates off its own line:

```text
A @ v = lambda * v
```

`lambda` (the corresponding **eigenvalue**) is how much `v` gets scaled. Most vectors get both rotated and scaled by `A`; eigenvectors are the special directions where only scaling happens.

This question restricts to **real symmetric** matrices (`A == A.T`) specifically because symmetric matrices are guaranteed to have real eigenvalues and orthogonal eigenvectors, a general square matrix can have complex eigenvalues (a rotation matrix, for instance, has no real eigenvector at all, it rotates every direction), which is a can of worms this question sidesteps on purpose. Symmetric matrices are also exactly the case that matters most in ML: a covariance matrix (used throughout the Probability and Unsupervised Learning tracks) is always symmetric, and PCA (`06-unsupervised`'s own PCA question) is literally "find the eigenvectors of the covariance matrix."

`np.linalg.eigh` (the `h` is for "Hermitian", the complex generalization of symmetric) is the specialized routine for exactly this case: it assumes symmetry, exploits it for both speed and numerical stability, and always returns real eigenvalues sorted ascending, with `eigenvectors[:, i]` the eigenvector belonging to `eigenvalues[i]`.

### How PyTorch actually implements this

`torch.linalg.eigh` (real PyTorch's equivalent) dispatches to LAPACK's symmetric eigensolver (`syevd`), a divide-and-conquer algorithm that is both asymptotically faster and more numerically stable than the general-purpose eigensolver (`geev`) `torch.linalg.eig` uses for arbitrary matrices, which is exactly why the specialized/general distinction from Theory isn't just pedagogical, it's a real, meaningful performance and stability choice a library makes for you when it can prove the matrix is symmetric. This machinery underlies `torch.pca_lowrank` and every real PCA implementation: rather than forming a covariance matrix and eigendecomposing it (numerically worse, and expensive for high-dimensional data), production code almost always computes the equivalent result via SVD directly on the data matrix instead, the connection `07-svd`, later in this track, makes explicit.

## Explanation

`eigen_decomposition` returns `np.linalg.eigh(a)` directly.

`verify_eigenpair` checks the defining equation from Theory directly: `A @ v` should equal `eigenvalue * v`, elementwise, within floating-point tolerance.
