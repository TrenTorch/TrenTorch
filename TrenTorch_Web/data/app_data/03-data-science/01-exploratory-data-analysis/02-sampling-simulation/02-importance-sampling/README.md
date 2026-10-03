---
name: data-science-importance-sampling
title: Importance Sampling
tags: [data-science, simulation, probability]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`01-monte-carlo` averages draws from the distribution of interest. That fails for rare events: to estimate the chance that a payment is fraudulent when one in a million is, a million draws contain one hit on average, and the estimate is noise. Importance sampling draws from a _different_ distribution that lands in the interesting region far more often, and then corrects for the switch by weighting each draw by how much more (or less) likely it is under the real distribution. It also lets one set of draws answer questions about several distributions. This question builds the estimator, its self-normalized version and the diagnostic that tells you whether the weights are trustworthy.

### From theory to code

Implement `importance_estimate(f, p_pdf, q_pdf, draws)`, the weighted average that estimates an expectation under `p` from draws taken under `q`, then `self_normalized_estimate(f, p_pdf, q_pdf, draws)`, which works even when `p` is known only up to a constant, then `effective_sample_size(weights)`, which measures how many equally good draws the weighted ones are worth. The signatures and docstrings are already in the editor.

### Constraints

- `draws` is a 1D float array of samples already taken from the proposal distribution `q`. `p_pdf` and `q_pdf` are vectorized functions returning the target and proposal densities at every draw. `f` is a vectorized function of the draws.
- `importance_estimate` returns `mean(f(draws) * w)` as a float, where `w = p_pdf(draws) / q_pdf(draws)`.
- `self_normalized_estimate` returns `sum(f(draws) * w) / sum(w)` as a float, with the same `w`. It must give the same answer if `p_pdf` is multiplied by any positive constant.
- `effective_sample_size(weights)` returns `sum(weights) ** 2 / sum(weights ** 2)` as a float, for a 1D array of non-negative weights with at least one positive entry.
- The proposal density must be positive wherever `p_pdf(x) * f(x)` is nonzero. Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

Reweighting is a change of measure: $\mathbb{E}_p[f] = \mathbb{E}_q[f \cdot p/q]$. Averaging $f \cdot p/q$ over draws from $q$ therefore estimates the expectation under $p$.

</details>

<details>
<summary>Hint 2</summary>

If $p$ is only known up to a constant (a posterior without its normalizing integral), the plain estimator is off by that constant. Dividing by the sum of the weights cancels it.

</details>

<details>
<summary>Hint 3</summary>

When a few weights are huge and the rest are tiny, the average is really made of a handful of draws. The effective sample size drops to close to that handful.

</details>

## Theory

### The simple version

Suppose you want to know how often a rare disease occurs, but you can only survey people at a specialist clinic, where it is far more common. Counting cases among clinic visitors would exaggerate the rate. If you know how much more likely a person with the disease is to be at the clinic than in the general population, you can down-weight each clinic case by that ratio and recover the true rate. Importance sampling does this in general: sample where the action is, then correct for having looked there.

### The formula

To estimate $\mathbb{E}_p[f(X)] = \int f(x)\,p(x)\,dx$ using draws $x_1, \dots, x_n$ from a proposal $q$, rewrite the integral with the **importance weight** $w(x) = p(x)/q(x)$:

$$
\mathbb{E}_p[f(X)] = \int f(x)\,\frac{p(x)}{q(x)}\,q(x)\,dx = \mathbb{E}_q\big[f(X)\,w(X)\big]
$$

so the estimator is

$$
\hat{\mu}_{\text{IS}} = \frac{1}{n}\sum_{i=1}^{n} f(x_i)\,w(x_i), \qquad w_i = \frac{p(x_i)}{q(x_i)}
$$

When $p$ is known only up to a constant, use the **self-normalized** form:

$$
\hat{\mu}_{\text{SN}} = \frac{\sum_i f(x_i)\,w_i}{\sum_i w_i}
$$

The constant cancels in the ratio. This estimator is slightly biased for finite $n$ but consistent, and it is the one used in practice.

The **effective sample size** measures how well the weights are spread:

$$
n_{\text{eff}} = \frac{\left(\sum_i w_i\right)^2}{\sum_i w_i^2}
$$

It equals $n$ when all weights are equal and approaches $1$ when one weight dominates.

### Choosing a proposal

The best proposal is large wherever $|f(x)|\,p(x)$ is large. A proposal that is _thinner in the tails_ than $p$ is dangerous: where $q$ is tiny but $p$ is not, the weight $p/q$ explodes, and one rare draw can swamp the whole estimate. A proposal with heavier tails than the target is the safe choice.

### Where this appears in machine learning

Off-policy evaluation in reinforcement learning reweights returns from an old policy by the ratio of action probabilities, which is importance sampling with the policy ratio as the weight (PPO clips this ratio to keep it from exploding). Importance-weighted autoencoders tighten the variational bound with it, and sequential Monte Carlo methods resample by importance weights.

### How NumPy/PyTorch actually implements this

`scipy.stats.norm.pdf` and similar give the densities. `np.average(f(x), weights=w)` is the self-normalized estimator in one call. `torch.distributions.Distribution.log_prob` provides log densities, and in practice weights are computed in log space (`log_w = log_p - log_q`) and normalized with `torch.softmax` or `logsumexp` to avoid overflow. `arviz.ess` reports effective sample sizes for sample sets.

## Explanation

`importance_estimate` forms the weight `p_pdf(draws) / q_pdf(draws)` for every draw, multiplies by `f(draws)` and averages, which is the change-of-measure identity from Theory. `self_normalized_estimate` uses the same weights but divides the weighted sum of `f` by the sum of the weights, so any constant factor on `p_pdf` appears in both numerator and denominator and cancels. `effective_sample_size` squares the sum of the weights and divides by the sum of the squared weights, which equals the number of draws when the weights are uniform and falls toward one as a single weight dominates.
