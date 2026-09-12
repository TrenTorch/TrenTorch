---
name: math-map-estimation
title: 'MAP estimation: maximum likelihood plus a prior'
tags: [probability]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`07-maximum-likelihood-estimation`'s MLE has a real weakness: with very little data, it trusts that small sample completely, 3 coin flips landing heads twice gives an MLE of 66.7% heads, even though you might have good reason to believe, before seeing any flips, that most coins are close to fair. MLE has no way to incorporate that prior belief, it only ever looks at the data in front of it.

MAP (Maximum A Posteriori) estimation fixes exactly this: it combines the likelihood (how well a parameter explains the data, MLE's whole criterion) with a prior (`05-bayes-theorem`'s prior belief, before seeing the data), and finds the parameter value that maximizes their product, the posterior. With a very informative prior and little data, MAP leans on the prior; with lots of data, MAP converges to the same answer MLE would give, the data eventually overwhelms any reasonable prior.

### From theory to code

Theory expresses the (unnormalized) log-posterior as the log-likelihood plus the log-prior, and, for the specific case of a Normal likelihood with a Normal prior on the mean, derives a closed-form MAP estimate: a precision-weighted average of the sample mean and the prior mean.

Implement `negative_log_posterior_normal(mean_candidate, x, data_std, prior_mean, prior_std)` (reusing `07-maximum-likelihood-estimation`'s NLL and `06-likelihood-vs-probability`'s `normal_pdf`), then `map_estimate_normal_mean(x, data_std, prior_mean, prior_std)`, the closed form.

### Constraints

- `data_std` is assumed known and fixed, only the mean is being estimated.
- `map_estimate_normal_mean` is closed-form, no search.
- With a very large `prior_std` (an uninformative prior), the MAP estimate should approach the plain sample mean (MLE).
- With a very small `prior_std` (an extremely confident prior), the MAP estimate should approach `prior_mean` itself.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`negative_log_posterior_normal` is a sum of two pieces you already have: the NLL of the data under `mean_candidate`, and the negative log of the prior's density AT `mean_candidate`.

</details>

<details>
<summary>Hint 2</summary>

"Precision" is `1 / variance`. The MAP mean is `(data_precision * sample_mean + prior_precision * prior_mean) / (data_precision + prior_precision)`, a weighted average where more precision (less variance, more confidence) means more weight.

</details>

## Theory

### The simple version

Before flipping a coin at all, most people already believe coins are usually close to fair, that's a prior. Flip it 3 times and get 2 heads, MLE would say "66.7% heads, full stop," ignoring everything you believed beforehand. MAP instead blends the two: your prior belief and what the 3 flips actually showed, weighted by how confident you are in each. With only 3 flips, your prior belief dominates (data this scarce doesn't override a reasonable prior). With 10,000 flips, the data dominates instead, at that point, no reasonable prior can hold out against that much evidence.

### The formula

Bayes' theorem (`05-bayes-theorem`) says `posterior ∝ likelihood * prior` (the evidence term is a constant with respect to the parameter, so it can be dropped when only maximizing over the parameter matters). In log-space:

```text
log(posterior) = log(likelihood) + log(prior) + constant
negative_log_posterior = negative_log_likelihood + negative_log_prior
```

For a Normal likelihood with known `data_std`, and a Normal prior on the mean with `prior_mean`/`prior_std`, setting the derivative of `negative_log_posterior` (with respect to the candidate mean) to zero gives a closed-form MAP estimate:

```text
data_precision  = n / data_std^2
prior_precision = 1 / prior_std^2

map_mean = (data_precision * sample_mean + prior_precision * prior_mean) / (data_precision + prior_precision)
```

**Precision** is just `1 / variance`, a measure of how confident a distribution is (low variance = high precision = high confidence). This formula is a precision-weighted average: the sample mean and prior mean each pull the estimate toward themselves, proportional to how confident (precise) that source is. Two limiting cases confirm this makes sense: as `prior_std -> infinity` (an infinitely uncertain, uninformative prior), `prior_precision -> 0`, and `map_mean -> sample_mean`, exactly MLE. As `prior_std -> 0` (an infinitely confident prior), `prior_precision -> infinity`, and `map_mean -> prior_mean`, the data can't move a belief that confident at all.

### How PyTorch actually implements this

L2 weight decay (`torch.optim`'s `weight_decay` parameter, seen throughout the Optimizers track) is MAP estimation in disguise: adding an `L2` penalty term to a loss function is mathematically equivalent to placing a Normal prior (centered at zero) on the network's weights and finding the MAP estimate instead of the plain MLE, "prefer smaller weights unless the data strongly justifies larger ones" is exactly a prior belief, expressed as a regularization term rather than an explicit Bayesian formula. This is the deep reason weight decay improves generalization: it's not an arbitrary penalty, it's encoding "most good solutions don't need extreme weight values" as a prior, the same role `prior_mean`/`prior_std` play here.

## Explanation

`negative_log_posterior_normal` sums `negative_log_likelihood_normal(x, mean_candidate, data_std)` (the data's contribution) and the negative log of `normal_pdf` evaluated at `mean_candidate` under the prior (the prior's contribution), exactly the log-space sum from Theory.

`map_estimate_normal_mean` computes both precisions (`n / data_std**2` and `1 / prior_std**2`) and combines the sample mean and prior mean into the precision-weighted average from Theory's closed-form derivation.
