---
name: data-science-mcmc-metropolis-hastings
title: Markov Chain Monte Carlo
tags: [data-science, simulation, probability, mcmc]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Monte Carlo estimation needs draws from a distribution. For many distributions that matter, such as the posterior of a Bayesian model, there is no way to draw from them directly: the density can be evaluated at any point, but only up to a constant, because the constant is an integral nobody can compute. Markov chain Monte Carlo gets around this by walking. A **Markov chain** takes a random step, proposes a move to a nearby point, and accepts or rejects the move with a probability designed so that, in the long run, the places the walker visits are distributed exactly like the target. This question builds the simplest and most widely used version, the Metropolis algorithm with Gaussian steps, and the tools to judge whether a chain can be trusted.

### From theory to code

Implement `metropolis_hastings(log_target, x0, n_steps, step_size, rng)`, which runs the walk, then `burn_in_and_thin(samples, burn_in, thin)`, which discards the early and redundant samples, then `autocorrelation(samples, lag)`, which measures how strongly each sample depends on the one `lag` steps earlier, then `mcmc_effective_sample_size(samples, max_lag)`, which turns that dependence into the number of independent samples the chain is worth. The signatures and docstrings are already in the editor.

### Constraints

- `log_target(x)` takes a float and returns the log of the target density, up to an additive constant. It may return `-inf` for points outside the support. The state is a single float.
- `metropolis_hastings` starts at `x0`. Each step draws, in this order, `step = rng.normal()` and then `u = rng.random()`. The proposal is `x_new = x + step_size * step`. It accepts when `log(u) < log_target(x_new) - log_target(x)`, otherwise it stays at `x`. The sample recorded for that step is the state after the accept or reject decision, so a rejected step repeats the previous value. It does not record `x0`.
- `metropolis_hastings` returns `(samples, acceptance_rate)`: a float array of length `n_steps` and the fraction of steps that accepted the proposal, as a float. The starting point must satisfy `log_target(x0) > -inf`.
- `burn_in_and_thin(samples, burn_in, thin)` returns `samples[burn_in::thin]` as a new array, for `burn_in >= 0` and `thin >= 1`.
- `autocorrelation(samples, lag)` returns the sample autocorrelation `sum((x[t] - m) * (x[t + lag] - m)) / sum((x[t] - m) ** 2)` with `m` the sample mean, summing `t` over `0 .. n - lag - 1`, as a float. At lag `0` it is `1.0`. It returns `0.0` if the sample has zero variance.
- `mcmc_effective_sample_size(samples, max_lag)` returns `n / (1 + 2 * sum(rho_k))` as a float, where `rho_k` is the autocorrelation at lag `k` and the sum runs over `k = 1, 2, ...` up to `max_lag`, stopping before the first lag whose autocorrelation is negative. The result is at least `1.0` and at most `n`.

### Hints

<details>
<summary>Hint 1</summary>

The acceptance rule never needs the normalizing constant of the target: the constant appears in both `log_target(x_new)` and `log_target(x)` and cancels in their difference. That cancellation is the reason the method works on unnormalized posteriors.

</details>

<details>
<summary>Hint 2</summary>

Compare in log space. A raw density ratio can overflow or underflow, while `log(u) < difference of logs` is stable. A move to a point with a higher density always has a difference above zero and is always accepted.

</details>

<details>
<summary>Hint 3</summary>

The effective sample size shrinks as the autocorrelation grows. If neighbouring samples are nearly copies of each other, thousands of them hold the information of a handful of independent draws.

</details>

## Theory

### The simple version

Picture a hiker dropped onto a foggy hillside at night who wants to spend time at each spot in proportion to how high it is, so that tall regions get visited often and low ones rarely. The hiker cannot see the whole hill, only the height at the current spot and at a spot a few steps away. The rule is: always step uphill, and step downhill only sometimes, with a chance equal to the ratio of the heights. Left to wander long enough, the trail the hiker leaves covers the hill in exactly the right proportions, with no map of the whole hill ever needed.

### The formula

The target density is $\pi(x)$, known only up to a constant: we can evaluate $\tilde{\pi}(x) \propto \pi(x)$. At state $x$ the **random-walk Metropolis** algorithm proposes

$$
x' = x + \sigma\,\varepsilon, \qquad \varepsilon \sim \mathcal{N}(0, 1)
$$

and accepts it with probability

$$
\alpha = \min\!\left(1,\ \frac{\tilde{\pi}(x')}{\tilde{\pi}(x)}\right)
$$

otherwise the chain stays at $x$. In log form: accept when $\log u < \log\tilde{\pi}(x') - \log\tilde{\pi}(x)$ with $u \sim \text{Uniform}(0,1)$.

- The proposal is symmetric (stepping from $x$ to $x'$ is as likely as from $x'$ to $x$), so no correction factor is needed. For an asymmetric proposal the full Metropolis-Hastings ratio multiplies by $q(x \mid x')/q(x' \mid x)$.
- The chain's stationary distribution is $\pi$, so after it has forgotten its starting point the visited states are (dependent) draws from $\pi$.

The **autocorrelation** at lag $k$ is

$$
\rho_k = \frac{\sum_{t=0}^{n-k-1}(x_t - \bar{x})(x_{t+k} - \bar{x})}{\sum_{t=0}^{n-1}(x_t - \bar{x})^2}
$$

and the **effective sample size** discounts the chain for its dependence:

$$
n_{\text{eff}} = \frac{n}{1 + 2\sum_{k=1}^{K}\rho_k}
$$

### Burn-in & thinning

The chain starts wherever `x0` is, which may be far from where the target has its mass. The early samples reflect that starting point rather than the target, so they are discarded as **burn-in**. **Thinning** keeps every few-th sample to reduce storage and the strong correlation between neighbours. It does not add information, and keeping every sample with a correct effective sample size is statistically better, but thinning is common for memory reasons.

### Tuning the step size

A tiny step is accepted almost always but crawls, so consecutive samples are nearly identical and the autocorrelation is high. A huge step lands in low-density regions and is almost always rejected, so the chain sits still. The efficient step is in between: for a one-dimensional Gaussian target an acceptance rate around 0.4 is near the best, and for many dimensions about 0.234 is the classic rule of thumb. The acceptance rate is the first dial to check.

### Checking a chain

A single chain cannot prove it has converged. Run several chains from different starting points and compare them (the Gelman-Rubin statistic), look at trace plots for drift, and compute the effective sample size. Multimodal targets are the hard case: a chain can stay in one mode for a very long time.

### How NumPy/PyTorch actually implements this

Production libraries use far more efficient samplers than random-walk Metropolis. `emcee`, `pymc`, `numpyro` and `Stan` use Hamiltonian Monte Carlo and its adaptive variant NUTS, which follow gradients of `log_target` and can be written with `torch.autograd` or JAX. `arviz.ess` and `arviz.rhat` compute the effective sample size and the Gelman-Rubin diagnostic. The accept-or-reject structure here is still the core of all of them.

## Explanation

`metropolis_hastings` keeps the current state and its log density, and for each step draws the normal step and then the uniform in the fixed order, forms the proposal, and accepts when `log(u)` is below the difference of log densities. It records the state after the decision, so a rejection repeats the previous sample, and counts accepts to return the acceptance rate. Working with logs means the unknown normalizing constant cancels in the difference and nothing underflows. `burn_in_and_thin` is a single slice that drops the first `burn_in` samples and keeps every `thin`-th after that. `autocorrelation` centers the series and divides the lagged sum of products by the zero-lag sum of squares, so lag zero is exactly one. `mcmc_effective_sample_size` adds up the autocorrelations from lag one until the first negative value or `max_lag` and divides `n` by `1 + 2 * sum`, then clips the result into `[1, n]`.
