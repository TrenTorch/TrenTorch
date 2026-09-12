---
name: math-bayes-theorem
title: "Bayes' theorem: updating a belief given evidence"
tags: [probability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A medical test for a rare disease comes back positive. Should you be worried? Your gut says "the test is 99% accurate, so I'm almost certainly sick," but that's the wrong question, it ignores how rare the disease was in the first place. If the disease affects 1 in 100 people, and even a small fraction of HEALTHY people also test positive (a false positive rate), the healthy false-positives can vastly outnumber the sick true-positives in raw counts, even with a 99%-accurate test. The right question is: "of everyone who tests positive, healthy and sick combined, what fraction are actually sick?"

Bayes' theorem is the formula that answers exactly this: it takes a prior belief (how common is the disease, before any test), combines it with how the evidence behaves under each hypothesis (how likely is a positive test if you're sick, vs if you're not), and produces the correct, updated belief (how likely are you sick, given the positive test).

### From theory to code

Theory gives the raw formula (`posterior = likelihood * prior / evidence`) and, for the common binary-hypothesis case, shows how to compute the evidence term yourself from the two conditional likelihoods and the prior.

Implement `bayes_theorem(prior, likelihood, evidence)` first, the direct formula, then `posterior_binary(prior_h, likelihood_e_given_h, likelihood_e_given_not_h)`, which computes the evidence term and calls the first function.

### Constraints

- All probabilities are plain floats in `[0, 1]`.
- `posterior_binary` must compute the evidence term itself (`P(evidence)`, the total probability of seeing the evidence at all, summed over both the H-true and H-false cases), not take it as a separate argument.
- `posterior_binary` should call `bayes_theorem` rather than reimplementing the same division.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`bayes_theorem` is one line: multiply, then divide.

</details>

<details>
<summary>Hint 2</summary>

The evidence term is a weighted average: `P(evidence | H) * P(H) + P(evidence | not H) * P(not H)`, and `P(not H) = 1 - P(H)`.

</details>

## Theory

### The simple version

Before any test, a random person has a small (say, 1%) chance of having a rare disease, that's your prior belief. Now they test positive. How much should that update your belief? It depends on two things you need to know about the test: how often it correctly flags sick people (true positive rate), and how often it WRONGLY flags healthy people (false positive rate). If healthy people vastly outnumber sick people (which they do, when a disease is rare), even a small false-positive rate can produce more false alarms than true detections, so a positive test moves your belief upward, but not nearly as far as "99% accurate" naively suggests.

### The formula

```text
posterior = P(H | evidence) = P(evidence | H) * P(H) / P(evidence)
                             = likelihood      * prior / evidence
```

- **Prior**, `P(H)`: what you believed before seeing any evidence.
- **Likelihood**, `P(evidence | H)`: how probable the evidence is, assuming the hypothesis is true.
- **Evidence**, `P(evidence)`: the total probability of seeing this evidence at all, under every possible hypothesis.
- **Posterior**, `P(H | evidence)`: your updated belief, after accounting for the evidence.

For a binary hypothesis (`H` true or false), the evidence term expands into two cases:

```text
P(evidence) = P(evidence | H) * P(H) + P(evidence | not H) * P(not H)
```

"The evidence could have come from the world where H is true, or the world where H is false, weighted by how likely each world was to begin with, and how likely the evidence is within each."

For the disease example (prior 1%, true positive rate 99%, false positive rate 5%): `P(evidence) = 0.99*0.01 + 0.05*0.99 = 0.0594`, and `P(H | positive test) = 0.99*0.01 / 0.0594 ~= 16.7%`, far below the naive "99% accurate means 99% sick" intuition, exactly the counterintuitive result Bayes' theorem exists to correct for.

### How PyTorch actually implements this

Naive Bayes classifiers (`02-naive-bayes-bernoulli`, `03-gaussian-naive-bayes`, in Classical ML) are literally this formula, applied at scale: the prior is how common each class is in the training data, the likelihood is `P(features | class)` estimated from the training data, and classification is choosing the class with the highest posterior. More broadly, Bayesian deep learning (a more advanced, less common paradigm than the standard training loops elsewhere in this curriculum) treats a network's weights themselves as a probability distribution updated via Bayes' theorem as training data arrives, rather than a single point estimate optimized by gradient descent, `06-bayesian-optimization` (Evaluation & Model Selection) is the one place in this curriculum's main path where this Bayesian-updating idea shows up directly, choosing which hyperparameters to try next based on a posterior belief about where the best ones are likely to be.

## Explanation

`bayes_theorem` computes `(likelihood * prior) / evidence` directly, the raw formula.

`posterior_binary` computes the evidence term as a weighted sum over both cases of the hypothesis (`likelihood_e_given_h * prior_h + likelihood_e_given_not_h * (1 - prior_h)`), then calls `bayes_theorem` with that computed evidence, reusing the first function rather than duplicating its division.
