---
name: math-positive-semidefinite-matrices
title: Positive Semi-Definite Matrices
tags: [linear-algebra, matrices, optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-positive-definite` asks that a quadratic form be strictly positive in every direction, so the bowl it describes has a single lowest point. Many matrices that matter in practice only meet a weaker bar: the form is never negative, but is allowed to be exactly zero along some direction, like a trough with a flat floor instead of a bowl. Covariance matrices and every matrix of the shape `X X^T` behave this way, and so does a Hessian at a flat spot. This question builds the weaker test, the family of matrices that always pass it, and a repair for matrices that should pass it and narrowly fail because of noise.

### From theory to code

Implement `is_positive_semidefinite(a, tol)`, which tests the weaker condition, then `gram_matrix(x)`, which builds a matrix that is positive semi-definite by construction, then `nearest_psd(a)`, which returns the closest positive semi-definite matrix to a given one. The signatures and docstrings are already in the editor.

### Constraints

- A matrix must be square and symmetric (within `np.allclose`) to be positive semi-definite. A non-symmetric matrix is not.
- Eigenvalues are only accurate to rounding error, so `is_positive_semidefinite` accepts an eigenvalue as zero if it is at least `-tol`. A genuinely negative eigenvalue such as `-1e-3` must still be rejected with the default `tol = 1e-10`.
- `gram_matrix(x)` takes an `m x d` array whose rows are vectors and returns the `m x m` matrix of all pairwise dot products of those rows.
- `nearest_psd(a)` returns a symmetric positive semi-definite matrix of the same shape. A non-symmetric input is first replaced by its symmetric part `(a + a.T) / 2`. The result must be the closest positive semi-definite matrix in Frobenius norm to that symmetric part.
- Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

Positive semi-definiteness is positive-definiteness with the strict inequality on the eigenvalues loosened to allow zero. The tolerance exists because an eigenvalue that is zero in exact arithmetic often comes out as a tiny negative number.

</details>

<details>
<summary>Hint 2</summary>

For `gram_matrix`, the quadratic form is `v^T (X X^T) v = ||X^T v||^2`, a squared length, which can never be negative. That is the whole reason this construction works.

</details>

<details>
<summary>Hint 3</summary>

Break the symmetric matrix into eigenvectors and eigenvalues. Replacing every negative eigenvalue with zero and rebuilding the matrix removes exactly the directions with negative curvature and changes nothing else.

</details>

## Theory

### The simple version

A positive-definite surface is a bowl: step away from the bottom in any direction and you climb. A positive semi-definite surface is a bowl that may have a flat valley running through it. You never go downhill, but in some direction you can walk forever without going uphill either. That flat direction is what allows a matrix to be singular and still behave well.

### The formula

A symmetric matrix $A$ is **positive semi-definite** (PSD) if

$$
x^{\top} A x \;\ge\; 0 \quad \text{for all } x
$$

Equivalently, every eigenvalue of $A$ is $\ge 0$, and equivalently $A = B^{\top} B$ for some matrix $B$.

- Strictly positive eigenvalues give positive-definite, which is a special case of PSD. A PSD matrix with a zero eigenvalue is **singular**, and the eigenvectors for that zero are the flat directions.
- A matrix of pairwise dot products, a **Gram matrix**, is always PSD. For rows $x_1, \dots, x_m$ the matrix $G = XX^{\top}$ has $G_{ij} = x_i \cdot x_j$, and $v^{\top} G v = \lVert X^{\top} v \rVert^2 \ge 0$. If the rows are linearly dependent, $G$ is singular.
- A covariance matrix is PSD for the same reason, since it is a Gram-style product of centered data.

### Repairing a matrix that should be PSD

Estimated covariance and kernel matrices are meant to be PSD but come out with a slightly negative eigenvalue after noise or rounding, which breaks routines that assume PSD such as a Cholesky factorization. The closest PSD matrix in Frobenius norm is found by writing $A = Q \Lambda Q^{\top}$ and clipping:

$$
A_{+} = Q \,\max(\Lambda, 0)\, Q^{\top}
$$

This is the **projection onto the PSD cone**. If $A$ is already PSD, it comes back unchanged.

### Where this shows up in machine learning

Covariance matrices, kernel matrices in SVMs and Gaussian processes, and Gauss-Newton approximations of Hessians are all PSD. A convex loss has a PSD Hessian everywhere, so gradient descent on it cannot get stuck at a saddle. Practical code clips or adds a small multiple of the identity to keep estimated matrices PSD before factorizing them.

### How NumPy/PyTorch actually implements this

`np.linalg.eigvalsh` returns the eigenvalues of a symmetric matrix in ascending order, so the first entry decides PSD-ness. `np.linalg.cholesky` succeeds for positive-definite matrices and raises an error otherwise, which is a common cheap definiteness probe. `torch.linalg.eigh` is the equivalent and also returns the eigenvectors needed for the clipping repair.

## Explanation

`is_positive_semidefinite` first rejects anything that is not square and symmetric under `np.allclose`, then takes the eigenvalues of the symmetric matrix with `np.linalg.eigvalsh` and checks that the smallest is at least `-tol`. The tolerance turns the exact condition `>= 0` into one that survives floating-point error without accepting real negative curvature. `gram_matrix` is simply `x @ x.T`, which is positive semi-definite for every input because each quadratic form is a squared length. `nearest_psd` averages the matrix with its transpose, takes the eigendecomposition with `np.linalg.eigh`, clips the eigenvalues at zero, and reassembles `Q diag(clipped) Q.T`, which is the Frobenius-closest PSD matrix to the symmetric part. It re-symmetrizes the result at the end to remove rounding asymmetry.
