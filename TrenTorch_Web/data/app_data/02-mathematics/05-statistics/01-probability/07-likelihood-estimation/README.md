---
name: math-likelihood-estimation
title: 'Likelihood & Estimation'
tags: [probability]
difficulty: Advanced
---

## Statement

### The problem, from first principles

**Likelihood vs probability**

"Given a fair coin, what's the chance of seeing 8 heads in 10 flips" and "given that I saw 8 heads in 10 flips, how fair was the coin" use the exact same binomial formula, plugged in two different ways. The first fixes the coin's fairness and asks about possible outcomes, that's a probability. The second fixes the outcome (it already happened) and asks about possible explanations, that's a likelihood. Same formula, same numbers even, but a completely different question being asked of it, and confusing the two is a genuinely common source of statistical mistakes.

This distinction underlies every "fit a model to data" question this curriculum poses: maximum likelihood estimation (the next question in this track) is precisely "find the parameter values that make the DATA YOU ACTUALLY OBSERVED look as likely as possible," which only makes sense once you've separated "probability of data, given parameters" from "likelihood of parameters, given data."

**Maximum likelihood**

`07-likelihood-estimation`'s `likelihood_curve` swept a grid of candidate means and evaluated each one, then you could squint at a plot and guess where the peak was. That's fine for one parameter and a hand-picked grid, but it doesn't scale, doesn't give an exact answer, and doesn't generalize to distributions with several parameters at once (mean AND std together).

Maximum likelihood estimation (MLE) is the principled version of "find where the likelihood curve peaks": instead of searching a grid, use calculus, set the derivative of the (log-)likelihood to zero and solve, to get an exact, closed-form answer directly. For a Normal distribution, this turns out to have a remarkably simple, familiar answer.

**MAP estimation**

`07-likelihood-estimation`'s MLE has a real weakness: with very little data, it trusts that small sample completely, 3 coin flips landing heads twice gives an MLE of 66.7% heads, even though you might have good reason to believe, before seeing any flips, that most coins are close to fair. MLE has no way to incorporate that prior belief, it only ever looks at the data in front of it.

MAP (Maximum A Posteriori) estimation fixes exactly this: it combines the likelihood (how well a parameter explains the data, MLE's whole criterion) with a prior (`04-conditional-bayes`'s prior belief, before seeing the data), and finds the parameter value that maximizes their product, the posterior. With a very informative prior and little data, MAP leans on the prior; with lots of data, MAP converges to the same answer MLE would give, the data eventually overwhelms any reasonable prior.

### From theory to code

**Likelihood vs probability**

Theory defines the Normal PDF once, then uses it two different ways: as a probability density over data (fixed parameters, varying data), and as a likelihood over parameters (fixed data, varying parameters). Implement the PDF once, a joint-density helper for a fixed parameter, and a likelihood curve that sweeps candidate parameter values against the SAME fixed data.

Implement `normal_pdf(x, mean, std)`, `joint_density(x_values, mean, std)` and `likelihood_curve(x_values, candidate_means, std)` against that reasoning. The signatures and docstrings are already in the editor.

**Maximum likelihood**

Theory works in log-space (summing log-densities rather than multiplying raw densities, for numerical stability) and derives closed-form MLE formulas for a Normal distribution's mean and standard deviation by setting derivatives to zero. Implement the log-space objective first (so you can numerically verify the closed forms against it), then the two closed-form estimators directly.

Implement `negative_log_likelihood_normal(x, mean, std)`, `mle_normal_mean(x)` and `mle_normal_std(x)` against that reasoning. The signatures and docstrings are already in the editor.

**MAP estimation**

Theory expresses the (unnormalized) log-posterior as the log-likelihood plus the log-prior, and, for the specific case of a Normal likelihood with a Normal prior on the mean, derives a closed-form MAP estimate: a precision-weighted average of the sample mean and the prior mean.

Implement `negative_log_posterior_normal(mean_candidate, x, data_std, prior_mean, prior_std)` (reusing `07-likelihood-estimation`'s NLL and `07-likelihood-estimation`'s `normal_pdf`), then `map_estimate_normal_mean(x, data_std, prior_mean, prior_std)`, the closed form.

### Constraints

**Likelihood vs probability**

- `normal_pdf` must vectorize over `x` (accept an array, return an array of the same shape).
- `joint_density` assumes every entry of `x_values` is independent, so their joint density is a product, not a sum.
- `likelihood_curve` calls `joint_density` once per candidate mean, holding `x_values` and `std` fixed throughout.

**Maximum likelihood**

- `negative_log_likelihood_normal` works in log-space (sum of `log(density)`), not `-log(product of densities)`.
- `mle_normal_mean` and `mle_normal_std` are closed-form (no search, no calls to `negative_log_likelihood_normal`).
- `mle_normal_std` divides by `n` (the biased estimator), not `n - 1`, Theory explains why MLE gives this specific version.

**MAP estimation**

- `data_std` is assumed known and fixed, only the mean is being estimated.
- `map_estimate_normal_mean` is closed-form, no search.
- With a very large `prior_std` (an uninformative prior), the MAP estimate should approach the plain sample mean (MLE).
- With a very small `prior_std` (an extremely confident prior), the MAP estimate should approach `prior_mean` itself.

### Hints

**Likelihood vs probability**

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`normal_pdf` is a direct, vectorized translation of the Gaussian formula, `np.exp` and `np.sqrt` handle arrays natively.

</details>

<details>
<summary>Hint 2</summary>

`joint_density` is `np.prod(normal_pdf(x_values, mean, std))`, one call reusing the function you already wrote.

</details>

**Maximum likelihood**

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`log(a * b * c) = log(a) + log(b) + log(c)`. Turn the product from `joint_density` into a sum of logs instead.

</details>

<details>
<summary>Hint 2</summary>

The MLE for the mean of a Normal distribution turns out to be exactly the plain sample average, no surprise formula needed.

</details>

**MAP estimation**

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

**Likelihood vs probability**

"Given a fair coin, how likely am I to see 8 heads out of 10 flips" fixes the coin (fair, 50/50) and asks about a possible outcome, that's a probability question. "I flipped a coin 10 times and got 8 heads, how fair was that coin, really" fixes what actually happened and asks which coin-fairness value best explains it, that's a likelihood question. Both questions can be answered using the exact same binomial formula, the only thing that changes is which variable you treat as fixed and which one you let vary.

**Maximum likelihood**

Imagine trying dozens of candidate "true averages" for a dataset and, for each one, asking "how likely would my actual data have been, if this were the true average?" The candidate that makes your actual, already-observed data look MOST likely is the maximum likelihood estimate. `07-likelihood-estimation` did exactly this by brute-force grid search; MLE does it with calculus instead, finding the peak exactly rather than approximately.

**MAP estimation**

Before flipping a coin at all, most people already believe coins are usually close to fair, that's a prior. Flip it 3 times and get 2 heads, MLE would say "66.7% heads, full stop," ignoring everything you believed beforehand. MAP instead blends the two: your prior belief and what the 3 flips actually showed, weighted by how confident you are in each. With only 3 flips, your prior belief dominates (data this scarce doesn't override a reasonable prior). With 10,000 flips, the data dominates instead, at that point, no reasonable prior can hold out against that much evidence.

### The formula

**Likelihood vs probability**

The Normal probability density function:

$$
\text{pdf}(x) = \frac{1}{\text{std} \cdot \sqrt{2\pi}} \exp\left(-\frac{1}{2}\left(\frac{x - \text{mean}}{\text{std}}\right)^2\right)
$$

Used as a **probability** (viewed as a function of `x`, with `mean` and `std` fixed): "how dense is the distribution at this particular data value?"

Used as a **likelihood** (the exact same function, viewed as a function of `mean` and `std`, with the observed `x` fixed): "how well does this particular choice of parameters explain the data I actually saw?"

For multiple independent observations, their joint probability density is the product of each one's individual density:

$$
\text{joint\_density}(x_1, \ldots, x_n \mid \text{mean}, \text{std}) = \prod_{i=1}^{n} \text{pdf}(x_i)
$$

A **likelihood curve** sweeps candidate parameter values against one FIXED dataset, using this same joint-density formula at every candidate. The parameter value where that curve peaks is the maximum likelihood estimate (the very next question in this track): the single choice of parameters that makes the observed data look as probable as possible, exactly what `likelihood_curve` computes one point at a time.

**Maximum likelihood**

Working with the log of the likelihood (rather than the raw product of densities) turns products into sums, both numerically safer (avoids underflow from multiplying many small numbers) and algebraically easier to differentiate:

$$
\text{log\_likelihood}(\text{mean}, \text{std} \mid x) = \sum_i \log\big(\text{normal\_pdf}(x_i, \text{mean}, \text{std})\big)
$$

$$
\text{negative\_log\_likelihood} = -\text{log\_likelihood}
$$

Since log is monotonic, maximizing the likelihood is equivalent to minimizing the negative log-likelihood, the form actually used here (and the form every loss function in `02-deep-learning-core` takes, cross-entropy and BCE are both negative log-likelihoods of their respective distributions).

Setting the derivative of the log-likelihood with respect to each parameter to zero and solving gives closed-form estimators for a Normal distribution:

$$
\text{mle\_mean} = \frac{1}{n}\sum_i x_i \quad \text{(the plain sample mean)}
$$

$$
\text{mle\_std} = \sqrt{\frac{1}{n}\sum_i \left(x_i - \text{mle\_mean}\right)^2} \quad \text{(the BIASED standard deviation)}
$$

The mean's MLE is exactly the ordinary average, no surprise. The std's MLE divides by `n`, not `n - 1`: `05-expectation-covariance`'s Bessel's correction exists specifically to counteract a bias that MLE, by its own derivation, does not correct for, MLE optimizes purely for "what explains my exact observed data best," and that criterion alone does not care about being unbiased across many hypothetical repeated samples, which is a different (and, for many practical purposes, more important) goal.

**MAP estimation**

Bayes' theorem (`04-conditional-bayes`) says `posterior ∝ likelihood * prior` (the evidence term is a constant with respect to the parameter, so it can be dropped when only maximizing over the parameter matters). In log-space:

$$
\log(\text{posterior}) = \log(\text{likelihood}) + \log(\text{prior}) + \text{constant}
$$

$$
\text{negative\_log\_posterior} = \text{negative\_log\_likelihood} + \text{negative\_log\_prior}
$$

For a Normal likelihood with known `data_std`, and a Normal prior on the mean with `prior_mean`/`prior_std`, setting the derivative of `negative_log_posterior` (with respect to the candidate mean) to zero gives a closed-form MAP estimate:

$$
\text{data\_precision} = \frac{n}{\text{data\_std}^2}
$$

$$
\text{prior\_precision} = \frac{1}{\text{prior\_std}^2}
$$

$$
\text{map\_mean} = \frac{\text{data\_precision} \cdot \text{sample\_mean} + \text{prior\_precision} \cdot \text{prior\_mean}}{\text{data\_precision} + \text{prior\_precision}}
$$

**Precision** is just `1 / variance`, a measure of how confident a distribution is (low variance = high precision = high confidence). This formula is a precision-weighted average: the sample mean and prior mean each pull the estimate toward themselves, proportional to how confident (precise) that source is. Two limiting cases confirm this makes sense: as `prior_std -> infinity` (an infinitely uncertain, uninformative prior), `prior_precision -> 0`, and `map_mean -> sample_mean`, exactly MLE. As `prior_std -> 0` (an infinitely confident prior), `prior_precision -> infinity`, and `map_mean -> prior_mean`, the data can't move a belief that confident at all.

### Try it live

**Likelihood vs probability**

<div class="tt-widget" data-widget="math-likelihood-vs-probability"></div>

**Maximum likelihood**

<div class="tt-widget" data-widget="math-maximum-likelihood-estimation"></div>

**MAP estimation**

<div class="tt-widget" data-widget="math-map-estimation"></div>

### How NumPy/PyTorch actually implements this

**Likelihood vs probability**

Every loss function `02-deep-learning-core` implements, `02-cross-entropy`, `03-binary-cross-entropy`, is a negative log-likelihood in disguise: minimizing cross-entropy loss is mathematically identical to maximizing the likelihood of the training labels under the model's predicted distribution. `torch.distributions.Normal(mean, std).log_prob(x)` computes exactly this question's `normal_pdf`, in log-space (for the same numerical-stability reasons `02-cross-entropy`'s log-softmax works in log-space rather than computing softmax then taking a log), and is the building block behind probabilistic models throughout deep learning, from VAEs to diffusion models, all of which are trained by maximizing some form of data likelihood.

**Maximum likelihood**

Training a neural network by minimizing cross-entropy or MSE loss IS maximum likelihood estimation, just for a distribution implicitly defined by the network's output rather than a simple Normal: minimizing MSE loss is exactly MLE under the assumption that residuals are Normally distributed with constant variance, and minimizing cross-entropy is exactly MLE under a categorical distribution defined by the softmax output. This is why `loss.backward()` on a well-chosen loss function isn't an arbitrary heuristic, it's gradient-based MLE, computing the same "which parameters make the observed data most likely" answer this question derives in closed form for the much simpler single-Normal case, but via numerical optimization instead of an exact formula (since a neural network's parameters don't admit one).

**MAP estimation**

L2 weight decay (`torch.optim`'s `weight_decay` parameter, seen throughout the Optimizers track) is MAP estimation in disguise: adding an `L2` penalty term to a loss function is mathematically equivalent to placing a Normal prior (centered at zero) on the network's weights and finding the MAP estimate instead of the plain MLE, "prefer smaller weights unless the data strongly justifies larger ones" is exactly a prior belief, expressed as a regularization term rather than an explicit Bayesian formula. This is the deep reason weight decay improves generalization: it's not an arbitrary penalty, it's encoding "most good solutions don't need extreme weight values" as a prior, the same role `prior_mean`/`prior_std` play here.

## Explanation

**Likelihood vs probability.** `normal_pdf` computes the Gaussian formula directly and vectorized, `np.exp` and array arithmetic apply elementwise automatically.

`joint_density` calls `normal_pdf` on the whole `x_values` array at once and multiplies every resulting density together via `np.prod`, the independent-observations product from Theory.

`likelihood_curve` calls `joint_density` once per entry of `candidate_means`, holding `x_values` and `std` fixed each time, producing the likelihood-as-a-function-of-parameters curve Theory describes.

**Maximum likelihood.** `negative_log_likelihood_normal` sums `log(normal_pdf(x_i, mean, std))` over every observation and negates, the log-space, numerically-safe version of the negative joint density.

`mle_normal_mean` returns `np.mean(x)`, the closed-form MLE derived in Theory.

`mle_normal_std` computes the mean first, then the root-mean-square deviation from it (`sqrt(mean((x - mean)^2))`), the biased closed-form MLE for standard deviation, dividing by `n` rather than `n - 1`.

**MAP estimation.** `negative_log_posterior_normal` sums `negative_log_likelihood_normal(x, mean_candidate, data_std)` (the data's contribution) and the negative log of `normal_pdf` evaluated at `mean_candidate` under the prior (the prior's contribution), exactly the log-space sum from Theory.

`map_estimate_normal_mean` computes both precisions (`n / data_std**2` and `1 / prior_std**2`) and combines the sample mean and prior mean into the precision-weighted average from Theory's closed-form derivation.
