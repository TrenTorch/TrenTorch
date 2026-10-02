---
name: math-definiteness-classification
title: Classifying Definiteness
tags: [linear-algebra, matrices, optimization]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The questions before this one each asked a yes-or-no about one kind of matrix: positive definite, positive semi-definite, negative definite, negative semi-definite. A symmetric matrix actually falls into exactly one of five classes, and the fifth is the one that causes trouble in optimization: a matrix that curves up in some directions and down in others, the shape of a mountain pass. Knowing which class the Hessian at a critical point belongs to is what tells you whether you have found a minimum, a maximum or a saddle. This question puts all five together and adds a second test, Sylvester's criterion, that decides positive definiteness from determinants alone.

### From theory to code

Implement `leading_principal_minors(a)`, the determinants of the top-left squares of a matrix, then `is_positive_definite_sylvester(a)`, which decides positive definiteness from them, then `classify_definiteness(a, tol)`, which names the class of a symmetric matrix, then `critical_point_type(hessian, tol)`, which turns that class into a verdict about a critical point. The signatures and docstrings are already in the editor.

### Constraints

- `leading_principal_minors(a)` takes a square `n x n` array and returns a 1D array of length `n` whose entry `k - 1` is the determinant of the top-left `k x k` block.
- `is_positive_definite_sylvester(a)` returns `True` only for a square symmetric matrix whose leading principal minors are all strictly positive. It must not compute eigenvalues.
- `classify_definiteness(a, tol)` requires a square symmetric matrix and raises `ValueError` otherwise. It returns exactly one of the strings `"positive definite"`, `"positive semidefinite"`, `"negative definite"`, `"negative semidefinite"`, `"indefinite"` or `"zero"`. An eigenvalue within `tol` of zero counts as zero, and `"zero"` is returned only when every eigenvalue is within `tol` of zero.
- `critical_point_type(hessian, tol)` returns `"local minimum"` for positive definite, `"local maximum"` for negative definite, `"saddle point"` for indefinite, and `"inconclusive"` for the semidefinite and zero cases. It raises `ValueError` for a non-symmetric Hessian.

### Hints

<details>
<summary>Hint 1</summary>

Count how many eigenvalues are clearly positive, clearly negative and within `tol` of zero. The class is a function of those three counts and nothing else.

</details>

<details>
<summary>Hint 2</summary>

Sylvester's criterion tests the determinants of the growing top-left squares. A single number that is not strictly positive anywhere in that list rules out positive definiteness.

</details>

<details>
<summary>Hint 3</summary>

Second-order information only decides the case when the curvature is nonzero in every direction. A semidefinite Hessian has a direction with zero curvature, so the second-order test cannot say more.

</details>

## Theory

### The simple version

Stand at a critical point of a smooth surface and look at how it bends in every direction. If every direction bends up, you are at the bottom of a bowl. If every direction bends down, you are on a hilltop. If some bend up and some bend down, you are on a saddle. If some directions are flat, the bend does not tell you enough and you have to look further. Those four situations, plus the all-flat zero matrix, are the whole story for a symmetric matrix.

### The five classes

For a symmetric matrix $A$ with eigenvalues $\lambda_1, \dots, \lambda_n$:

| Class                  | Eigenvalues                     | $x^{\top} A x$           |
| ---------------------- | ------------------------------- | ------------------------ |
| Positive definite      | all $> 0$                       | $> 0$ for all $x \neq 0$ |
| Positive semi-definite | all $\ge 0$, at least one $= 0$ | $\ge 0$ for all $x$      |
| Negative definite      | all $< 0$                       | $< 0$ for all $x \neq 0$ |
| Negative semi-definite | all $\le 0$, at least one $= 0$ | $\le 0$ for all $x$      |
| Indefinite             | some $> 0$ and some $< 0$       | takes both signs         |

The zero matrix is both positive and negative semi-definite, so it is reported as its own case. Every nonzero symmetric matrix falls in exactly one of the five rows.

### Sylvester's criterion

The **leading principal minors** $D_k$ are the determinants of the top-left $k \times k$ blocks. A symmetric matrix is positive definite exactly when

$$
D_1 > 0,\; D_2 > 0,\; \dots,\; D_n > 0
$$

and negative definite exactly when the signs alternate starting negative, $(-1)^k D_k > 0$ for every $k$. This avoids computing eigenvalues, which is useful for a quick hand check on a small matrix. It works only for the strict classes. A matrix such as $\mathrm{diag}(0, -1)$ has $D_1 = D_2 = 0$ yet is negative semi-definite, so deciding semi-definiteness needs **every** principal minor, not only the leading ones, and the eigenvalue route is simpler.

### From classes to critical points

At a point where the gradient is zero, the second-order Taylor expansion (`02-taylor`) is governed by the Hessian $H$ (`05-hessian-matrix`):

$$
f(x_0 + d) \approx f(x_0) + \tfrac{1}{2}\, d^{\top} H d
$$

so the sign of $d^{\top} H d$ in each direction $d$ says whether $f$ rises or falls that way. Positive definite gives a **local minimum**, negative definite a **local maximum**, and indefinite a **saddle point**. For a semi-definite Hessian some direction has zero second-order change, so the test is **inconclusive** and higher-order terms decide.

### Where this shows up in machine learning

Saddle points, not poor local minima, are the typical obstacle in high-dimensional training. Their Hessians are indefinite, which is why plain gradient descent slows near them and why second-order and noise-injection methods help. A convex problem has a positive semi-definite Hessian everywhere. Newton's method is only safe to step along when the Hessian is positive definite, and trust-region and damping schemes exist to repair the indefinite case.

### How NumPy/PyTorch actually implements this

`np.linalg.eigvalsh` gives the eigenvalue signs directly. `np.linalg.det` on slices `a[:k, :k]` gives the minors. `np.linalg.cholesky` succeeds exactly when a symmetric matrix is positive definite, and is what libraries use as the fast check. `torch.autograd.functional.hessian` produces the Hessian matrix whose class this question decides.

## Explanation

`leading_principal_minors` takes `np.linalg.det` of each growing top-left block `a[:k, :k]` for `k` from 1 to `n`. `is_positive_definite_sylvester` returns `False` for anything non-square or non-symmetric, then checks that every minor is strictly positive, never touching an eigenvalue. `classify_definiteness` validates the matrix, takes the eigenvalues with `np.linalg.eigvalsh`, and counts how many are above `tol`, below `-tol` and within `tol` of zero. All zeros gives `"zero"`, positives only gives definite or semidefinite depending on whether any zero eigenvalue is present, negatives only mirrors that, and both signs present gives `"indefinite"`. `critical_point_type` is a lookup from that class to the verdict, with every semidefinite and zero class mapped to `"inconclusive"` because a flat direction hides what the second-order term cannot see.
