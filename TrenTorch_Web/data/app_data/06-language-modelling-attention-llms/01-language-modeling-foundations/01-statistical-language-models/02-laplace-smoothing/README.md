---
name: lm-laplace-smoothing
title: Laplace Smoothing
tags: [language-modeling, smoothing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Counts become probabilities by dividing each row by its total. That is the maximum-likelihood estimate, and it has a sharp flaw: any pair you never saw gets probability exactly zero. One unseen pair in a test word then makes the whole word impossible, and its log-probability becomes minus infinity. A language model should be a little humble about what it has not observed. Adding a small pseudo-count `alpha` to every cell before normalizing shifts a sliver of probability from the common pairs to the unseen ones, so nothing is ever impossible.

### From theory to code

Implement `smoothed_probabilities(counts, alpha)`, which turns a count matrix into a row-stochastic probability matrix with add-`alpha` smoothing.

### Constraints

- `counts` is a non-negative `(V, V)` array and `alpha > 0`.
- Return `(counts + alpha) / (row total + alpha * V)` so each row sums to 1.
- Do not modify `counts`.
- A row of all zeros becomes the uniform distribution.

### Hints

<details>
<summary>Hint 1</summary>

Add `alpha` to the whole matrix, then divide each row by its own sum with `keepdims=True` so broadcasting divides row by row.

</details>

<details>
<summary>Hint 2</summary>

The denominator is just the row sum of the smoothed matrix, so no separate formula is needed.

</details>

## Theory

### The simple version

A baker asks a hundred customers which pie they like. If nobody mentioned rhubarb, the raw tally says nobody will ever want rhubarb. Pretending each pie got a few extra imaginary votes keeps the popular pies on top but leaves rhubarb with a small, honest chance.

### The formula

$$
P(j \mid i) = \frac{N_{ij} + \alpha}{\sum_{k}\left(N_{ik} + \alpha\right)} = \frac{N_{ij} + \alpha}{N_{i\cdot} + \alpha V}
$$

With $\alpha = 1$ this is Laplace smoothing. As $\alpha \to 0$ it approaches the maximum-likelihood estimate and as $\alpha \to \infty$ it approaches the uniform distribution.

### How this is done in practice

Libraries expose the same knob under different names: `alpha` in scikit-learn's `MultinomialNB`, the `gamma` of `nltk.lm.Laplace`, and Kneser-Ney or back-off schemes when a single constant is too crude. The pseudo-count is a Bayesian prior in disguise: it is the posterior mean under a symmetric Dirichlet prior.

## Explanation

Smoothing is one vectorised expression. Adding `alpha` everywhere guarantees every cell is positive, and dividing by the smoothed row sum restores a valid distribution. The row total grows by exactly `alpha * V`, which is why the denominator above has that term. Rows that were entirely zero come out uniform, which is the right answer when there is no evidence at all.
