---
name: instance-based-probabilistic-spectral-drift-gp-calibration
title: 'SPECTRAL DRIFT'
tags: [classical-ml, probabilistic, gaussian-processes, physics, production-ml]
difficulty: Advanced
---

## Statement

**Difficulty:** Hard
**Tags:** Physics (Atomic Spectra), Gaussian Processes, Bayesian Regression, Production ML

---

### Story

You're building calibration software for a teaching-lab spectrometer that measures the
hydrogen emission spectrum. Theory (the Rydberg formula) tells you exactly what wavelength
each electron transition _should_ produce. In practice, every measured line comes out
slightly off from theory — the grating has a small systematic drift that varies smoothly
with wavelength (thermal expansion, imperfect alignment), plus a bit of random measurement
noise.

You don't know the drift function in closed form, but you know it's _smooth_: two nearby
wavelengths will have similar calibration error, while two very different wavelengths might
not. That "similar inputs → similar outputs, with smoothness as the only real assumption" is
exactly what a **Gaussian Process** models. You'll place a GP prior over the calibration-drift
function, condition it on your measured lines, and use the posterior to predict — with
honest uncertainty — the true wavelength of hydrogen lines you haven't measured yet,
including ones far outside your training range.

---

### The Physics: hydrogen spectral lines

An electron transition from energy level `n2` down to level `n1` (integers, `1 ≤ n1 < n2`)
emits a photon whose wavelength in vacuum is given by the **Rydberg formula**:

```
1/λ = R_H · (1/n1² - 1/n2²)
```

**Use exactly `R_H = 1.097373 × 10⁷ m⁻¹`** throughout (do not substitute a different
textbook value — this fixes the reference answer precisely). Convert `λ` to **nanometers**
(`1 m = 10⁹ nm`) for all input/output in this problem. `n1 = 1` gives the Lyman series,
`n1 = 2` the Balmer series (visible light), `n1 = 3` the Paschen series (infrared), and so on
— the different series live in very different, widely separated wavelength ranges.

For each training measurement you are given the transition `(n1, n2)` and the _measured_
wavelength. Compute the _theoretical_ wavelength `x` from the Rydberg formula, and define the
**calibration residual** `y = measured - theoretical`. This `(x, y)` pair — theoretical
wavelength vs. measured-minus-theoretical drift — is the data your GP will be trained on.

---

### The ML: Gaussian Process Regression

Model the drift function `f` with a zero-mean GP prior and a **squared-exponential (RBF)**
kernel with hyperparameters `σ_f` (signal std. dev.), `l` (length scale, nm), both `> 0`:

```
k(x, x') = σ_f² · exp( -(x - x')² / (2l²) )
```

Observations are noisy: `y_i = f(x_i) + ε_i`, `ε_i ~ N(0, σ_n²)`, with given noise std. dev.
`σ_n > 0`.

Given `n` training pairs `(x_i, y_i)`, build the `n×n` kernel matrix `K` with
`K_ij = k(x_i, x_j)`, and for any query input `x*` the exact GP posterior is:

```
mean:      μ(x*) = k*ᵀ (K + σ_n² I)⁻¹ y
variance:  σ²(x*) = k(x*, x*) - k*ᵀ (K + σ_n² I)⁻¹ k*
```

where `k* = [k(x_1, x*), ..., k(x_n, x*)]ᵀ` and `y = [y_1, ..., y_n]ᵀ`. Note
`k(x*, x*) = σ_f²` always (the kernel's value at zero distance).

**You must solve the linear systems via Cholesky decomposition** of `K + σ_n² I` (it is
guaranteed positive definite), not by explicitly forming a matrix inverse — standard GP
practice, and necessary here to stay numerically stable when `σ_n` is small and training
points are close together in `x`.

For each query transition `(n1*, n2*)`, compute its theoretical wavelength `x*` from the
Rydberg formula, then output:

```
predicted wavelength = x* + μ(x*)          (the calibration-corrected estimate)
uncertainty          = sqrt(σ²(x*))         (posterior standard deviation, nm)
```

---

### Input Format

```
n
n1_1 n2_1 measured_1
n1_2 n2_2 measured_2
...
n1_n n2_n measured_n
sigma_f l sigma_n
m
q_n1_1 q_n2_1
q_n1_2 q_n2_2
...
q_n1_m q_n2_m
```

- `n1_i, n2_i, q_n1_i, q_n2_i` are positive integers with `n1 < n2` (a valid transition).
- `measured_i` is the measured wavelength in **nanometers**.
- `sigma_f, l, sigma_n` are the GP hyperparameters described above (all `> 0`).

### Output Format

Print `m` lines, each with two numbers separated by a space: the predicted (corrected)
wavelength in nm, and the posterior uncertainty (std. dev.) in nm — both to at least 6
digits after the decimal point.

**Judging:** accepted if within `1e-4` absolute or relative error (whichever is larger) of
the reference solution, for **both** numbers on each line independently.

---

### Constraints

- `1 ≤ n ≤ 100`
- `1 ≤ m ≤ 100`
- `1 ≤ n1 < n2 ≤ 30` for every training and query transition
- `measured_i` given with up to 6 decimal digits, guaranteed within `1` nm of the true
  theoretical wavelength for that transition (i.e. realistic calibration drift, not garbage
  data)
- `0 < sigma_f ≤ 10`, `0 < l ≤ 10^4`, `0 < sigma_n ≤ 1`
- `K + σ_n² I` is guaranteed numerically positive definite (no duplicate training `x` values
  with `σ_n` too small to compensate)
- Time limit: 2 seconds. Memory limit: 256 MB.

---

### Example 1

**Input**

```
3
2 3 656.3
2 4 486.15
2 5 434.10
0.2 50.0 0.05
2
2 6
1 2
```

**Output**

```
410.195499 0.091764
121.502291 0.200000
```

**Explanation:** The three Balmer training lines (Hα, Hβ, Hγ) all show a similar positive
drift (≈ +0.14 to +0.19 nm), so the GP infers a smooth, mostly-positive correction across that
wavelength region. Query `(2,6)` (Hδ, theoretical `410.070231` nm) falls right inside the
training range, so it gets a confident, sizeable correction (`+0.125268` nm, uncertainty
shrinks well below `σ_f = 0.2`). Query `(1,2)` (Lyman-α, theoretical `121.502291` nm) is
_extremely_ far in wavelength from every training point — the RBF kernel correlation there
is essentially zero, so the posterior reverts exactly to the GP prior: **zero** correction
and uncertainty exactly `σ_f = 0.2`.

---

### Example 2

**Input**

```
4
2 3 656.28
2 4 486.12
2 5 434.08
2 6 410.05
0.15 20.0 0.02
2
2 7
3 4
```

**Output**

```
396.851586 0.083163
1874.606772 0.150000
```

**Explanation:** Four Balmer lines this time, with a shorter length scale (`l=20`) so
correlations fade faster with distance. Query `(2,7)` (theoretical `396.907483` nm) sits just
past the training range and still gets a meaningful correction (`-0.055897` nm) because it's
within about one length-scale of the nearest training point. Query `(3,4)` is a **Paschen**
series line — theoretical wavelength `1874.606772` nm, over a thousand nanometers from every
Balmer training point — so again the posterior reverts exactly to the prior: zero correction,
uncertainty exactly `σ_f = 0.15`.

## Theory

### Why a Gaussian Process, not a parametric curve fit

A polynomial or spline fit commits to a fixed functional form and gives you a single "best"
curve with no principled notion of how much to trust it far from the data. A GP instead
places a probability distribution directly over _functions_: before seeing any data, every
smooth function is a candidate, weighted by the kernel's notion of smoothness; after
conditioning on the training residuals, the functions inconsistent with the data are ruled
out, and what's left is a posterior distribution whose mean is the best-guess correction curve
and whose variance is an honest, calibrated uncertainty — exactly what a calibration tool
needs to report along with every corrected wavelength.

### What the kernel actually encodes

The squared-exponential kernel `k(x, x') = σ_f² exp(-(x-x')²/(2l²))` says: two inputs `x` and
`x'` produce highly correlated function values when they're close together (relative to `l`),
and essentially uncorrelated values once their distance exceeds a few multiples of `l`. `σ_f`
sets the overall scale of the function's variation; `l` sets _how far_ "nearby" reaches. This
is precisely why a query transition from a totally different spectral series — thousands of
nanometers from any training point — gets no real correction: the kernel correlation between
that query and every training point is essentially zero, so the posterior mean stays at zero
and the posterior variance reverts to the prior variance `σ_f²`.

### Why Cholesky, not a direct inverse

`(K + σ_n²I)⁻¹` is mathematically well-defined, but explicitly computing a matrix inverse is
both slower (`O(n³)` with a much larger constant than a single factorization) and numerically
worse — small eigenvalues in `K` (which happen exactly when training points are close together
in `x`, a case this problem explicitly tests) get amplified by direct inversion in a way a
triangular solve doesn't. Cholesky factors the symmetric positive-definite matrix once as
`K + σ_n²I = LLᵀ`, then both the training-time weight vector `α` and every query's posterior
mean/variance reduce to solving two triangular systems (forward-substitute `Lz = y`, then
back-substitute `Lᵀα = z` — repeated with `k*` in place of `y` for each query's variance
term), each `O(n²)` instead of needing the full inverse at all.

## Explanation

`rydberg_wavelength_nm` implements the Rydberg formula directly, converting the result from
meters to nanometers. `gp_calibrate` first turns every training row into an `(x_i, y_i)` pair
(theoretical wavelength, measured-minus-theoretical residual), builds the `n×n` RBF kernel
matrix, adds `σ_n²` to the diagonal, and Cholesky-factors the result once via
`np.linalg.cholesky`. `_forward_substitution` and `_back_substitution` solve the two
triangular systems by hand (no `np.linalg.inv`, no `np.linalg.solve` on the full matrix) to
get the weight vector `alpha`. For each query, it computes the query's theoretical wavelength,
the kernel vector `k*` against every training point, the posterior mean via `k* @ alpha`, and
the posterior variance via a second forward-substitution solve (`Lv = k*`) followed by
`σ_f² - v @ v` — clamped at zero to guard against a tiny negative value from floating-point
rounding when the true variance is essentially zero. The final output pairs each query's
corrected wavelength (`x* + μ(x*)`) with its uncertainty (`sqrt(σ²(x*))`).
