---
name: support-vector-machines-the-margin-deterministic-smo
title: 'THE MARGIN'
tags: [classical-ml, svm, optimization, quadratic-programming, production-ml]
difficulty: Advanced
---

## Statement

**Difficulty:** Hard
**Topic:** Deterministic Sequential Minimal Optimization (SMO), Constrained Quadratic Programming, Production ML

---

### Story

You work on the fraud-detection team at a payments company. You've settled on a linear
max-margin classifier (SVM) as the model — it's simple, fast at inference time, and legally
easy to explain to auditors. But compliance has one hard requirement: the trained model must
be **bit-for-bit reproducible**. Standard SMO implementations (like libsvm) pick which pair
of variables to optimize using heuristics that involve iteration order and tie-breaking that
differ across library versions — unacceptable when a regulator asks you to retrain last
quarter's model and get the *exact same* decision boundary back.

So your team defines its own fully deterministic training procedure: a **simplified,
cyclic-pairing SMO** — no randomness, no heuristic pair selection, just a fixed rule anyone
can re-implement and get identical results. Your job is to implement it exactly as specified
below, train it on the labeled transaction data, and report the model's raw decision score on
new transactions.

---

### Input Format

```
n d
x_1,1 x_1,2 ... x_1,d y_1
x_2,1 x_2,2 ... x_2,d y_2
...
x_n,1 x_n,2 ... x_n,d y_n
C tol max_passes
m
q_1,1 q_1,2 ... q_1,d
...
q_m,1 q_m,2 ... q_m,d
```

- `y_i ∈ {-1, +1}` (integers)
- `C` — box constraint, `0 < C ≤ 1000`
- `tol` — KKT violation tolerance, `0 < tol ≤ 1`
- `max_passes` — number of consecutive no-change passes required to stop

### Output Format

Print `m` lines: the raw decision score `f(q)` for each query, with at least 6 digits after
the decimal point.

**Judging:** accepted if within `1e-4` absolute or relative error (whichever is larger) of
the reference implementation's output, which follows the algorithm above **exactly**,
including its exact stopping rule — this is intentionally a specific deterministic procedure,
not "run until true convergence to the QP optimum," so implementations that reach the true
optimum by a different path will *not* generally match.

---

### Constraints

- `1 ≤ n ≤ 200`
- `1 ≤ d ≤ 20`
- `1 ≤ m ≤ 200`
- `1 ≤ max_passes ≤ 1000`
- All feature values satisfy `|value| ≤ 10^4`, given with up to 6 decimal digits.
- No two training feature vectors are identical.
- Time limit: 3 seconds. Memory limit: 256 MB.

---

### Example 1

**Input**
```
4 2
2 2 1
3 3 1
0 0 -1
1 0 -1
1.0 0.001 10
2
2 0
0.5 2
```

**Output**
```
-0.600000
0.400000
```

**Explanation:** Running the deterministic cyclic SMO to convergence (`max_passes = 10`
consecutive clean passes) on this small linearly separable set gives `α = [0.4, 0, 0, 0.4]`
(points `(2,2)` and `(1,0)` become the support vectors) and `b = -1.4`. Then
`f(2,0) = 0.4·1·(2·2+2·0) + 0.4·(-1)·(1·2+0·0) - 1.4 = 0.4·4 - 0.4·2 - 1.4 = -0.6`, and
similarly `f(0.5,2) = 0.4`.

---

### Example 2

**Input**
```
4 2
2 2 1
3 3 1
0 0 -1
1 0 -1
0.25 0.001 5
2
2 0
0.5 2
```

**Output**
```
-0.625000
0.000000
```

**Explanation:** Same data, but now `C = 0.25` is small enough to actively clip both support
vectors: the algorithm converges with `α = [0.25, 0, 0, 0.25]`, `b = -1.125`. This shows the
box constraint binding — with the earlier `C=1.0` the unconstrained-by-box optimum needed
`α = 0.4` per support vector, so lowering `C` below that forces clipping and changes both `b`
and every downstream prediction, even though the *support vectors themselves* (which training
points end up with nonzero `α`) are unchanged.

---

### Hidden Test Categories

1. **Box-constraint binding** — `C` small enough that the optimal (unconstrained) `α` values
   would exceed it, forcing clipping to `L`/`H` on nearly every relevant pair.
2. **Skip-condition correctness** — data engineered so `L = H` occurs for some pairs and the
   `|Δα_j| < 1e-5` no-op threshold is hit for others; a common bug is treating "skip" the same
   as "converged" and terminating the whole pass early instead of just moving to the next `i`.
3. **Multiple full sweeps before convergence** — `n` large enough (up to `200`) that several
   passes with real updates occur before `max_passes` consecutive clean passes are observed;
   checks the `passes` counter reset-on-change logic.
4. **Non-separable-looking clusters** (still no duplicate points) — where many points end up
   as support vectors simultaneously, exercising the `b1`/`b2`/averaged-`b` branch broadly.
5. **`max_passes = 1`** — an intentionally under-trained model; checks contestants aren't
   silently "finishing the job" by running to true optimality instead of stopping exactly on
   schedule.
6. **High-dimensional, few points** (`d` close to `20`, `n` small) — checks the dot-product
   kernel and gradient bookkeeping generalize beyond 2D.
7. **Tight `tol`** vs. **loose `tol`** on the same dataset, producing different numbers of
   updates and different final `α`/`b` — checks the KKT-check inequality directions
   (`< -tol` / `> tol`) are implemented exactly, not with the sign flipped.
8. **Live-update sensitivity** — datasets specifically constructed so that using `f_now`
   computed from *stale* (pre-pass) `α` instead of the live, mid-pass-updated `α` produces a
   detectably different numeric answer, catching a batch-vs-sequential-update bug.

## Theory

### The Math

You are given `n` labeled training points `(x_i, y_i)`, `x_i ∈ ℝ^d`, `y_i ∈ {-1, +1}`, and a
box constraint `C`. Using the linear kernel `K(x, z) = x · z`, the SVM **dual** problem is:

$$
\max_{\alpha} \ W(\alpha) = \sum_i \alpha_i - \frac{1}{2}\sum_i \sum_j \alpha_i \alpha_j y_i y_j K(x_i, x_j)
\qquad \text{s.t. } 0 \le \alpha_i \le C,\ \ \sum_i \alpha_i y_i = 0
$$

Once `alpha` and bias `b` are known, the decision function is:

$$
f(q) = \sum_i \alpha_i y_i K(x_i, q) + b
$$

This is the same dual-optimization idea `Margin maximization intuition` and
`Linear SVM via gradient descent on hinge loss` approach from two different directions: the
first reasons about the margin geometrically, the second reaches an equivalent boundary by
gradient descent on the *primal* objective (hinge loss plus an L2 penalty). This question
solves the *dual* directly, which is what real production SVM solvers (libsvm, scikit-learn's
`SVC`) actually do internally, and is exactly why the dual introduces `alpha`, one weight per
training point, rather than one weight per feature dimension.

#### Why a deterministic solver, not the textbook SMO

Textbook SMO picks the pair of `alpha`s to update at each step using heuristics (largest KKT
violation, iteration caches, etc.) precisely because that speeds up convergence in practice.
But those heuristics involve floating-point comparisons whose tie-breaking and iteration order
can differ subtly across library versions and even across runs, exactly the property that
breaks bit-for-bit reproducibility. Trading some convergence speed for a fully fixed, cyclic
pairing rule (`j` is always `i`'s next index, wrapping around) removes that ambiguity
completely: given the same data and the same `C`/`tol`/`max_passes`, the result is bitwise
identical every time, by construction.

#### The training loop

Initialize every `alpha_i` to `0`, `b` to `0`, and a `passes` counter to `0`. A **pass** is one
full sweep over every training index `i = 0 .. n-1`, in order. For each `i` in that sweep:
compute how badly point `i` currently violates the KKT stationarity conditions (`E_i`, the
gap between its current raw score and its true label). If it's violated by more than `tol`
(and there's room to move `alpha_i` in the direction that would fix it), pair `i` with its
fixed partner `j = (i+1) mod n` and jointly update `alpha_i` and `alpha_j`, the two-variable
update SMO is named for, since the dual's `sum(alpha_i * y_i) = 0` constraint means no single
`alpha` can move alone without breaking it: moving `alpha_j` by some amount forces `alpha_i`
to move by a matching amount in the opposite direction (scaled by `y_i` and `y_j`) to keep
the sum at zero.

Every update is computed from the **live** state of `alpha` and `b`, not a snapshot taken at
the start of the pass: an update made at index `2` is immediately visible to the KKT check at
index `3` in that same sweep. This is what makes the "cyclic" part of "cyclic-pairing SMO"
actually converge in a bounded, predictable way, an update chain can propagate information
across the whole training set within a single pass, rather than needing one full pass per
single point's worth of progress.

A pass with zero real updates increments `passes`; a pass with at least one real update resets
`passes` back to `0`. Training stops the moment `passes` reaches `max_passes`: that many
*consecutive* clean passes in a row, not `max_passes` passes total. This is why `max_passes`
is better read as "how sure do we need to be that nothing is left to update" rather than "how
long do we train for": a dataset that needs several rounds of updates before finally settling
will still run those rounds regardless of `max_passes`, since a dirty pass always resets the
counter back to zero.

#### The two-variable update itself

For a chosen pair `(i, j)`, the box constraint `0 <= alpha <= C` plus the equality constraint
`sum(alpha * y) = 0` together restrict how far `alpha_j` is allowed to move: those bounds
`L` and `H` depend on whether `y_i` and `y_j` agree (their sum, not their difference, is what
stays fixed when labels match) or disagree (their difference stays fixed instead). If `L`
equals `H`, there's no room to move at all, and this pair is skipped, exactly as if it hadn't
violated KKT in the first place. Otherwise, the *unconstrained* optimal step for `alpha_j`
comes from a one-dimensional quadratic in `alpha_j` alone (`eta`, the curvature of that
quadratic, is always negative for two distinct points under the linear kernel, since it works
out to `-‖x_i - x_j‖²`), and the result gets clipped back into `[L, H]` if it overshoots.
`alpha_i` then moves by exactly the amount needed to keep the equality constraint intact.

Finally, `b` is recomputed from whichever of the two updated points still sits strictly inside
the box (`0 < alpha < C`, meaning it's a genuine, non-clipped support vector, since the KKT
stationarity condition pins down `b` exactly at such a point); if both points ended up at a
box boundary instead, any `b` in a certain valid range would technically satisfy KKT there, so
the two candidate values are averaged as a stable, deterministic tiebreak.

## Explanation

`smo_fit` precomputes the full linear-kernel Gram matrix `K = X @ X.T` once (the kernel never
changes across passes, only `alpha` and `b` do), then runs the pass loop exactly as specified:
for each index `i` in order, it evaluates `E_i` from the *current* `alpha`/`b` (never a
snapshot), checks the KKT-violation condition, and on a violation pairs `i` with
`j = (i+1) % n`. It computes the box bounds `L`/`H` from whether `y_i` and `y_j` agree, skips
if they're equal, computes `eta` and skips if it's non-negative (the guard the problem
requires even though the no-duplicate-points guarantee means it never actually fires), solves
for the clipped `alpha_j`, skips again if the resulting change is below the `1e-5` threshold,
derives the matching `alpha_i` update, and picks `b` from whichever updated variable is
strictly inside the box (or averages both candidates if neither is). A pass with zero real
changes increments the `passes` counter; any real change resets it to `0`, and the loop stops
the instant `passes` reaches `max_passes`. `svm_decision_function` reuses the same linear
kernel (as `queries @ X.T`) to compute `f(q) = sum_i(alpha_i * y_i * K(x_i, q)) + b` for every
query row in one vectorized pass.
