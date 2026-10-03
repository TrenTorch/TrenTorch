---
name: agentic-retry-with-backoff
title: Exponential Backoff & Jitter
tags: [agentic-systems, reliability, retries, tools]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Tool calls fail for transient reasons: a rate limit, a timeout, an overloaded server. Retrying immediately usually fails again and, worse, a crowd of clients retrying in lockstep keeps the server overloaded. The standard remedy is **exponential backoff**: wait `base`, then `base * factor`, then `base * factor^2`, up to a cap, so the load on the struggling service falls quickly. Adding **jitter**, a random fraction of the delay, desynchronizes clients so that they do not all return at the same instant. "Full jitter" waits a uniformly random time between 0 and the capped delay.

### From theory to code

Implement `backoff_delays` and `total_wait`.

### Constraints

- `backoff_delays(n_retries, base, factor, cap, rng=None)` returns a list of `n_retries` waiting times. Retry `k` (starting at 0) has `capped = min(cap, base * factor ** k)`.
- If `rng` is `None` the delay is `capped`. Otherwise it is full jitter: `capped * rng.random()`, with exactly one `rng.random()` call per retry in order (`rng` is a `random.Random`).
- `total_wait(delays)` returns the sum as a float.

### Hints

<details>
<summary>Hint 1</summary>

Compute the capped schedule first, then multiply by the random draws.

</details>

<details>
<summary>Hint 2</summary>

The cap stops the delay from growing without bound after a few retries.

</details>

## Theory

### The simple version

Knocking on a door that nobody answers: do not knock again at once, wait a little, then longer, and never so long you forget. If a hundred people knock at the same rhythm they block each other, so each picks a random wait.

### The formula

$$
d_k = \min\big(c,\; b\,m^{k}\big), \qquad d_k^{\text{jitter}} = U_k\, d_k,\; U_k \sim \text{Uniform}(0, 1)
$$

Without a cap, the total wait after $n$ retries is the geometric sum $b\,(m^n - 1)/(m - 1)$.

### How this is done in practice

AWS's architecture blog popularized full jitter, and libraries such as `tenacity` and the OpenAI and Anthropic SDKs implement it. Retries should only be applied to idempotent or deduplicated calls, which is the subject of the durable-execution questions in this track.

## Explanation

The schedule is deterministic apart from the random multiplier, so seeding the generator makes the delays reproducible. Passing the generator in makes the randomness injectable and testable.
