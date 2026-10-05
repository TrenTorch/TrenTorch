---
name: lm-pass-at-k
title: Pass@k Estimation
tags: [evaluation, code-generation, sampling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Code and math benchmarks have a checker: a response is simply right or wrong. Since models sample, one attempt per problem is a noisy measurement, and a useful question is "if I let the model try `k` times, how often does at least one attempt pass". The obvious estimate, draw exactly `k` samples per problem and count successes, has high variance. Better: draw `n >= k` samples, observe that `c` of them passed, and compute the probability that a random subset of size `k` of those `n` contains at least one success. That estimate is **unbiased** and uses all `n` samples.

### From theory to code

Implement `pass_at_k` and `mean_pass_at_k`.

### Constraints

- `pass_at_k(n, c, k)` is `1 - C(n - c, k) / C(n, k)` for `1 <= k <= n` and `0 <= c <= n`. Return exactly `1.0` when `n - c < k`.
- Compute it as `1 - prod_{i = n - c + 1}^{n} (1 - k / i)`. Do not build binomial coefficients: they overflow for large `n`.
- `mean_pass_at_k(ns, cs, k)` averages `pass_at_k` over problems, where each problem can have a different number of samples. Return a Python float.
- `k = 1` must give `c / n`.

### Hints

<details>
<summary>Hint 1</summary>

When `c = 0` the product is empty and the estimate is `0.0`.

</details>

<details>
<summary>Hint 2</summary>

Rewrite the ratio of binomials as a telescoping product so every factor is between 0 and 1.

</details>

## Theory

### The simple version

You rolled a die ten times and got one six. How likely is it that three rolls picked at random from those ten include the six? It is 1 minus the chance that all three picks avoid it. That is exactly this estimator, with a sample of generations in place of dice.

### The formula

$$
\text{pass@}k = 1 - \frac{\binom{n - c}{k}}{\binom{n}{k}}
= 1 - \prod_{i=n-c+1}^{n}\Big(1 - \frac{k}{i}\Big)
$$

The probability that a uniformly random size-$k$ subset of the $n$ samples contains no passing sample is $\binom{n-c}{k}/\binom{n}{k}$.

### How this is done in practice

This estimator comes from the HumanEval paper and is implemented in `evaluate` and every code-generation harness. Larger `k` rewards diversity and a strong verifier, which is why pass@k is also the headline quantity when a model is used with best-of-n selection or in reinforcement learning with verifiable rewards.

## Explanation

The product form is numerically safe for any `n`. The early return covers the case where fewer than `k` samples failed, so any size-`k` subset must contain a success. Averaging over problems with different `n` supports adaptive sampling budgets.
