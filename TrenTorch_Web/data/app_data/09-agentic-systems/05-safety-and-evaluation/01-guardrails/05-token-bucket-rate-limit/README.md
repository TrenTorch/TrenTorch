---
name: agentic-token-bucket-rate-limit
title: Token Bucket Rate Limiting
tags: [agentic-systems, safety, rate-limiting, budgets]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

An autonomous agent can issue calls far faster than any person, so it needs a speed limit: on API calls, emails sent, files written. The **token bucket** is the standard way to enforce one that allows short bursts but caps the long-run rate. Picture a bucket holding up to `capacity` tokens. Each action removes one token (or more for expensive actions). Tokens drip back in at `refill_rate` per second. A full bucket allows a burst of `capacity` quick actions, and an empty bucket forces the agent to wait for tokens. As in the circuit breaker, time is passed in so that the behaviour is deterministic.

### From theory to code

Implement the class `TokenBucket`.

### Constraints

- `TokenBucket(capacity, refill_rate)` starts **full** at time `0.0`.
- `try_acquire(now, n=1)`: first refill by `refill_rate * (now - last_time)`, capped at `capacity`, and set `last_time = now`. If at least `n` tokens are available, subtract `n` and return `True`; otherwise leave the tokens unchanged and return `False`.
- `now` never decreases between calls. `tokens` is an attribute holding the current (float) token count after the last call.

### Hints

<details>
<summary>Hint 1</summary>

Refill before every decision, including failed ones, so the clock always advances.

</details>

<details>
<summary>Hint 2</summary>

A request for more than `capacity` tokens can never succeed.

</details>

## Theory

### The simple version

A water tank with a slow refill: you can take a lot at once if it is full, but if you keep taking, you are limited to the refill speed.

### The formula

$$
\text{tokens}(t) = \min\big(C,\ \text{tokens}(t') + r\,(t - t')\big), \qquad \text{allow} \iff \text{tokens}(t) \ge n
$$

Over a long window $T$ at most $C + rT$ tokens can be consumed.

### How this is done in practice

Token buckets limit API traffic in gateways such as Envoy, NGINX and Stripe's public API, and agent frameworks use them to cap tool calls and model spend. Leaky buckets and sliding windows are alternatives with different burst behaviour.

## Explanation

The refill-then-check structure is the entire algorithm. The tests probe the burst, the steady state and the cap on accumulation.
