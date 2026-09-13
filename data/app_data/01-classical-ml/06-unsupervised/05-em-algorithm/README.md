---
name: unsupervised-em-algorithm
title: 'Stretch: EM Algorithm'
tags: [classical-ml, unsupervised, clustering, gaussian-mixture, stretch]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`04-gaussian-mixture` built two individual moves: given parameters, compute responsibilities (E-step); given responsibilities, re-estimate parameters (M-step). Neither move alone fits a model — you have to actually alternate them, starting from some initial guess, and keep going until the parameters settle. That's the same "build the primitive, then assemble the loop" split `03-best-split-minimal-tree` used for a single tree split versus full recursion, and `04-full-boosting-loop` used for one boosting round versus the whole training loop.

The other missing piece is knowing whether the loop is actually helping. With gradient descent you'd watch a loss go down; here the natural quantity to watch is the mixture's total log-likelihood of the data — how well the current parameters explain what was actually observed. EM comes with an unusually strong guarantee about that quantity, one most iterative algorithms in this curriculum can't make: each E-step/M-step pair can only increase it, never decrease it.

### From theory to code

Implement `gmm_log_likelihood(input, weights, means, variances)`, which scores how well a given set of mixture parameters explains `input`, and `fit_gmm(input, n_components, max_iter, seed=None)`, which initializes parameters and repeatedly calls `04-gaussian-mixture`'s `gmm_e_step`/`gmm_m_step`, tracking `gmm_log_likelihood` after each iteration. Theory below derives the log-likelihood formula as a log-sum-exp over the same per-component scores `gmm_e_step` already computes; the loop itself is just calling the two existing functions in sequence.

### Constraints

- Reuse `04-gaussian-mixture`'s `gmm_e_step`/`gmm_m_step` — don't reimplement either.
- `gmm_log_likelihood` returns a single float: the total log-likelihood of `input` under the given `(weights, means, variances)`.
- Must be numerically stable — a point far from every component's mean must not produce `-inf` or `nan`.
- `fit_gmm` initializes means from `n_components` distinct rows of `input` (sampled without replacement, using `seed` for reproducibility), uniform starting weights, and every component starting with `input`'s overall per-feature variance.
- `fit_gmm` returns a dict with `"weights"`, `"means"`, `"variances"` (final, post-loop), `"responsibilities"` (from the _last_ E-step), and `"log_likelihood_history"` (array, one entry per iteration, recorded after that iteration's M-step).
- The loop runs exactly `max_iter` iterations, always E-step then M-step.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`gmm_log_likelihood` needs the same `log(weights[j]) + gaussian_log_likelihood(input[i], means[j], variances[j])` matrix `gmm_e_step` builds internally. The difference is what you do with each row afterward: `gmm_e_step` normalizes a row into a probability distribution; here you need the row's _un-normalized total_, in log space.

</details>

<details>
<summary>Hint 2</summary>

"Sum a row of log-values, in log space, stably" is log-sum-exp: subtract the row's max, exponentiate, sum, take the log, then add the max back. Skipping the max-subtraction is exactly what breaks on a point whose true probability under every component underflows to exactly `0.0`.

</details>

<details>
<summary>Hint 3</summary>

For `fit_gmm`'s initialization, `rng.choice(n_samples, n_components, replace=False)` picks distinct row indices — index `input` with them to get starting means. The loop body itself is just two calls: feed the current parameters into `gmm_e_step` to get responsibilities, then feed those into `gmm_m_step` to get the next parameters, and score the result with `gmm_log_likelihood` before moving to the next iteration.

</details>

## Theory

### The simple version

Imagine adjusting a set of dials (the mixture's weights, means, variances) to make a story fit some observed data as well as possible. EM does this in two alternating moves: first, hold the dials fixed and figure out, given today's story, how each data point probably arose (which component it likely came from) — that's the E-step. Then, hold those probable origins fixed and adjust the dials to better fit the data given that story — that's the M-step. Repeating this can only ever make the story fit at least as well as before, never worse — there's no equivalent of gradient descent overshooting and making things worse.

### The formula

The total log-likelihood being climbed:

```
log_likelihood = sum_i log( sum_j weights[j] * P(x_i | component j) )
```

Computed stably by reusing the per-sample-per-component log score:

```
log_probs[i, j] = log(weights[j]) + gaussian_log_likelihood(x_i, means[j], variances[j])
```

then log-sum-exp per row instead of `gmm_e_step`'s normalize-per-row:

```
max_log[i]    = max_j log_probs[i, j]
per_sample[i] = max_log[i] + log( sum_j exp(log_probs[i, j] - max_log[i]) )
log_likelihood = sum_i per_sample[i]
```

The training loop:

```
initialize weights, means, variances
repeat max_iter times:
    responsibilities = gmm_e_step(input, weights, means, variances)
    weights, means, variances = gmm_m_step(input, responsibilities)
    record gmm_log_likelihood(input, weights, means, variances)
```

### How PyTorch actually implements this

The log-sum-exp step is exactly what `torch.logsumexp` computes (subtract-max, exponentiate, sum, log, add max back, all in one stable call). EM itself is a general algorithm, not a specific `torch` API — `tests.py` verifies the real EM guarantee directly (`test_log_likelihood_never_decreases_across_iterations`, `test_more_iterations_never_decreases_final_log_likelihood`) rather than comparing against a baked external-library oracle, since the guarantee itself is the thing worth checking.

## Explanation

`gmm_log_likelihood` builds `log_probs[i, j]` (solution.py lines 22-27) with the identical `np.log(weights[j]) + gaussian_log_likelihood(input[i], means[j], variances[j])` expression `gmm_e_step` uses in `04-gaussian-mixture` — same inputs, same per-pair score. Where `gmm_e_step` normalizes each row into a probability distribution, this function instead computes `max_log = log_probs.max(axis=1, keepdims=True)` (line 29) and `per_sample = max_log[:, 0] + np.log(np.sum(np.exp(log_probs - max_log), axis=1))` (line 30) — the log-sum-exp of each row, giving the log of that sample's total mixture density without ever exponentiating an unshifted (and potentially very negative) log-probability. `test_log_likelihood_is_numerically_stable_for_extreme_values` targets exactly the failure this avoids: a point 1000 units from every component's mean, whose raw probability would underflow to `0.0` and make `log(0)` blow up to `-inf` without the shift. `float(np.sum(per_sample))` (line 31) sums these per-sample values into the single total log-likelihood.

`fit_gmm` initializes with `init_idx = rng.choice(n_samples, n_components, replace=False)` then `means = input[init_idx].copy()` (lines 38-39) — real data points as starting means, a standard, simple GMM initialization; `weights = np.full(n_components, 1.0 / n_components)` (line 40) starts every component with equal mixing weight; `variances = np.tile(input.var(axis=0), (n_components, 1))` (line 41) gives every component the same overall per-feature variance as a neutral starting spread, refined once real iterations begin. The loop (lines 45-48) calls `gmm_e_step` then `gmm_m_step` in sequence exactly `max_iter` times, appending `gmm_log_likelihood(input, weights, means, variances)` — evaluated on the _just-updated_ parameters — to `log_likelihood_history` each time, which is the sequence `test_log_likelihood_never_decreases_across_iterations` checks is monotonically non-decreasing (allowing `-1e-6` slack for floating-point noise, not a real decrease).
