---
name: math-likelihood-vs-probability
title: 'Likelihood vs. probability: the same formula, two different questions'
tags: [probability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

"Given a fair coin, what's the chance of seeing 8 heads in 10 flips" and "given that I saw 8 heads in 10 flips, how fair was the coin" use the exact same binomial formula, plugged in two different ways. The first fixes the coin's fairness and asks about possible outcomes, that's a probability. The second fixes the outcome (it already happened) and asks about possible explanations, that's a likelihood. Same formula, same numbers even, but a completely different question being asked of it, and confusing the two is a genuinely common source of statistical mistakes.

This distinction underlies every "fit a model to data" question this curriculum poses: maximum likelihood estimation (the next question in this track) is precisely "find the parameter values that make the DATA YOU ACTUALLY OBSERVED look as likely as possible," which only makes sense once you've separated "probability of data, given parameters" from "likelihood of parameters, given data."

### From theory to code

Theory defines the Normal PDF once, then uses it two different ways: as a probability density over data (fixed parameters, varying data), and as a likelihood over parameters (fixed data, varying parameters). Implement the PDF once, a joint-density helper for a fixed parameter, and a likelihood curve that sweeps candidate parameter values against the SAME fixed data.

Implement `normal_pdf(x, mean, std)`, `joint_density(x_values, mean, std)` and `likelihood_curve(x_values, candidate_means, std)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `normal_pdf` must vectorize over `x` (accept an array, return an array of the same shape).
- `joint_density` assumes every entry of `x_values` is independent, so their joint density is a product, not a sum.
- `likelihood_curve` calls `joint_density` once per candidate mean, holding `x_values` and `std` fixed throughout.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`normal_pdf` is a direct, vectorized translation of the Gaussian formula, `np.exp` and `np.sqrt` handle arrays natively.

</details>

<details>
<summary>Hint 2</summary>

`joint_density` is `np.prod(normal_pdf(x_values, mean, std))`, one call reusing the function you already wrote.

</details>

## Theory

### The simple version

"Given a fair coin, how likely am I to see 8 heads out of 10 flips" fixes the coin (fair, 50/50) and asks about a possible outcome, that's a probability question. "I flipped a coin 10 times and got 8 heads, how fair was that coin, really" fixes what actually happened and asks which coin-fairness value best explains it, that's a likelihood question. Both questions can be answered using the exact same binomial formula, the only thing that changes is which variable you treat as fixed and which one you let vary.

### The formula

The Normal probability density function:

```text
pdf(x) = (1 / (std * sqrt(2*pi))) * exp(-0.5 * ((x - mean) / std)^2)
```

Used as a **probability** (viewed as a function of `x`, with `mean` and `std` fixed): "how dense is the distribution at this particular data value?"

Used as a **likelihood** (the exact same function, viewed as a function of `mean` and `std`, with the observed `x` fixed): "how well does this particular choice of parameters explain the data I actually saw?"

For multiple independent observations, their joint probability density is the product of each one's individual density:

```text
joint_density(x_1, ..., x_n | mean, std) = pdf(x_1) * pdf(x_2) * ... * pdf(x_n)
```

A **likelihood curve** sweeps candidate parameter values against one FIXED dataset, using this same joint-density formula at every candidate. The parameter value where that curve peaks is the maximum likelihood estimate (the very next question in this track): the single choice of parameters that makes the observed data look as probable as possible, exactly what `likelihood_curve` computes one point at a time.

### How PyTorch actually implements this

Every loss function `02-deep-learning-core` implements, `02-cross-entropy`, `03-binary-cross-entropy`, is a negative log-likelihood in disguise: minimizing cross-entropy loss is mathematically identical to maximizing the likelihood of the training labels under the model's predicted distribution. `torch.distributions.Normal(mean, std).log_prob(x)` computes exactly this question's `normal_pdf`, in log-space (for the same numerical-stability reasons `02-cross-entropy`'s log-softmax works in log-space rather than computing softmax then taking a log), and is the building block behind probabilistic models throughout deep learning, from VAEs to diffusion models, all of which are trained by maximizing some form of data likelihood.

## Explanation

`normal_pdf` computes the Gaussian formula directly and vectorized, `np.exp` and array arithmetic apply elementwise automatically.

`joint_density` calls `normal_pdf` on the whole `x_values` array at once and multiplies every resulting density together via `np.prod`, the independent-observations product from Theory.

`likelihood_curve` calls `joint_density` once per entry of `candidate_means`, holding `x_values` and `std` fixed each time, producing the likelihood-as-a-function-of-parameters curve Theory describes.
