---
name: math-trace-of-a-matrix
title: 'Trace of a Matrix and Its Invariance Properties'
tags: [linear-algebra]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The **trace** is the smallest, cheapest-to-compute summary a square matrix has — just its diagonal entries, added up. It sounds almost too simple to matter, but it shows up constantly: as a fast way to compute the sum of a matrix's eigenvalues without finding any of them, inside the KL divergence formula for two multivariate Gaussians, and inside regularization terms that penalize a weight matrix's overall scale.

### From theory to code

Implement `trace(A)`, summing `A`'s diagonal entries, then `trace_of_product(A, B)`, computing `trace(A @ B)` — but doing it in a way that reveals a useful shortcut identity, covered in Theory. The signatures and docstrings are already in the editor.

### Constraints

- `A` is a square 2D NumPy array (`n × n`).
- For `trace_of_product`, `A` is `(m, n)` and `B` is `(n, m)`, so `A @ B` is a valid `(m, m)` square matrix.

### Hints

<details>
<summary>Hint 1</summary>

`trace(A)` is `Σ_{i} A[i, i]` — `01-summation-notation`'s `Σ` applied directly to the diagonal, or equivalently `np.diag(A).sum()`.

</details>

<details>
<summary>Hint 2</summary>

`trace(A @ B)` and `trace(B @ A)` are always equal even when `A @ B` and `B @ A` are entirely different-shaped matrices (or not even both defined) — you don't need to actually form the full product `A @ B` to compute its trace; summing `(A * B.T)` element-wise and then summing that result computes the same number more directly. Try implementing it the direct way (`np.trace(A @ B)`) first, then think about why the shortcut works.

</details>

## Theory

### The simple version

A matrix's diagonal is the handful of entries that map "input direction `i`" straight back onto "output direction `i`," undistorted by mixing with any other direction. The trace adds those up into one number — a rough, single-value summary of "how much this matrix scales things along their own original directions, on average," ignoring everything about how it mixes directions together off the diagonal.

### The formula

$$
\text{tr}(A) = \sum_{i=1}^{n} A_{ii}
$$

- `A_{ii}` — the diagonal entries: row `i`, column `i`, for each `i` from `1` to `n`.
- `tr(A)` — their sum, a single scalar, defined only for square matrices (a non-square matrix has no well-defined diagonal running corner to corner).

### The trace-of-a-product identity, and why it holds

For matrices `A` (shape `m × n`) and `B` (shape `n × m`), a genuinely useful identity holds:

$$
\text{tr}(AB) = \text{tr}(BA)
$$

even though `AB` is `m × m` and `BA` is `n × n` — potentially entirely different sizes. This follows directly from expanding both sides using `01-linear-algebra`'s `Matrix multiplication` definition: `tr(AB) = Σ_i (AB)_{ii} = Σ_i Σ_k A_{ik} B_{ki}`, and `tr(BA) = Σ_k (BA)_{kk} = Σ_k Σ_i B_{ki} A_{ik}` — the same double sum over `i` and `k`, just written with the two summation symbols in the opposite order, which doesn't change a finite sum's total. This identity, called the **cyclic property of trace**, is what lets `tr(A @ B)` be computed as `(A * B.T).sum()` without ever materializing the full `A @ B` matrix — genuinely useful when `A @ B` would be enormous but you only ever need its trace.

### Where this shows up

- **Eigenvalues**: the trace of a matrix always equals the sum of its eigenvalues (`06-eigenvalues-eigenvectors`), even though computing eigenvalues directly is far more expensive than just summing the diagonal.
- **KL divergence between two multivariate Gaussians** (Information Theory / Common Distributions tracks): the closed-form formula includes a `tr(Σ₂⁻¹Σ₁)` term, directly comparing the two distributions' covariance matrices' overall scale.
- **Frobenius norm**: `‖A‖_F² = tr(AᵀA)` — squaring and summing every entry of `A` is the same number as taking the trace of `AᵀA`, a fact that follows from the same double-sum expansion used above.

### How NumPy actually implements this

`np.trace(A)` computes the diagonal sum directly; for the shortcut identity, `np.sum(A * B.T)` (element-wise multiply, then sum everything) computes `tr(A @ B)` without ever forming the full product, which matters when `A @ B` would be a large matrix you have no other use for.

## Explanation

`trace(A)` returns `np.diag(A).sum()`, reading off the diagonal entries directly and adding them. `trace_of_product(A, B)` returns `np.sum(A * B.T)` — the cyclic-property shortcut from Theory, computing the same number as `np.trace(A @ B)` would, but without forming the potentially large intermediate product `A @ B` at all, only ever touching arrays already the same size as the inputs.
