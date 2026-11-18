---
name: agentic-pass-hat-k-reliability
title: Reliability with pass^k
tags: [agentic-systems, evaluation, reliability, pass-hat-k]
difficulty: Advanced
---

## Statement

### The problem, from first principles

For code generation, pass@k asks "if I try `k` times, does at least one attempt succeed?", which suits a user who can pick the best answer. An **agent that acts on behalf of a customer** has the opposite requirement: it must succeed **every time**, because an agent that cancels the wrong order one time in five is not usable. **pass^k** measures this: the probability that **all** `k` independent attempts at a task succeed. Estimated from `n` trials with `c` successes, it is the chance that a random size-`k` subset of those trials is all successes, `C(c, k) / C(n, k)`. It drops quickly as `k` grows for an agent that is merely "usually right", which is exactly why it reveals unreliability that pass@1 hides.

### From theory to code

Implement `pass_hat_k` and `mean_pass_hat_k`.

### Constraints

- `pass_hat_k(n, c, k)` is `C(c, k) / C(n, k)` for `1 <= k <= n` and `0 <= c <= n`. Compute it as the product `prod_{i=0}^{k-1} (c - i) / (n - i)`; return exactly `0.0` when `c < k`.
- `mean_pass_hat_k(ns, cs, k)` averages over tasks (each with its own `n` and `c`) and returns a float.
- For `k = 1` the result is the ordinary success rate `c / n`.

### Hints

<details>
<summary>Hint 1</summary>

The product form avoids huge binomial coefficients.

</details>

<details>
<summary>Hint 2</summary>

Once a factor `(c - i)` reaches 0 the whole product is 0.

</details>

## Theory

### The simple version

A pilot who lands safely 9 times out of 10 sounds good. A hundred landings in a row without incident is a very different bar, and the 90% pilot is unlikely to clear it.

### The formula

$$
\text{pass}^k = \frac{\binom{c}{k}}{\binom{n}{k}} = \prod_{i=0}^{k-1}\frac{c - i}{n - i}, \qquad
\text{pass@}k = 1 - \frac{\binom{n - c}{k}}{\binom{n}{k}}
$$

For a task with true success probability $p$: $\text{pass}^k \to p^k$ and $\text{pass@}k \to 1 - (1-p)^k$.

### How this is done in practice

pass^k was introduced with the tau-bench benchmark for customer-service agents, which showed strong models dropping sharply as `k` increases. Reporting it alongside pass@1 distinguishes an agent that is good on average from one that is dependable.

## Explanation

A short product and an average. The tests contrast it with pass@k on the same data, which is the point of the question: the two rise and fall in opposite directions as `k` grows.
