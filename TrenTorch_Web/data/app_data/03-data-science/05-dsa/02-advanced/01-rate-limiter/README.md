---
name: dsa-rate-limiter
title: 'Rate Limiter (Token Bucket)'
tags: [dsa]
difficulty: Advanced
---

## Statement

Design a rate limiter using the token bucket algorithm. Implement a `RateLimiter` class that:

- Allows up to `capacity` requests within a `window` time window
- Issues tokens at a constant rate
- Rejects requests when no tokens are available
- Tracks the last refill time to compute available tokens

Write methods:

- `__init__(capacity, refill_rate)`: capacity tokens, refill_rate tokens per second
- `is_allowed(tokens_needed=1)`: returns True if tokens are available, False otherwise
- `refill()`: issue new tokens based on elapsed time

### Constraints

- O(1) time per request
- Handle concurrent requests safely (optional: use threading locks if needed)

### Hints

<details>
<summary>Hint 1</summary>

Track the last refill timestamp and compute elapsed time since then.

</details>

<details>
<summary>Hint 2</summary>

Each request consumes tokens; refill calculates new tokens based on elapsed seconds.

</details>

## Theory

### Token Bucket Algorithm

Rate limiting prevents API abuse by restricting request frequency. Token bucket is a classical algorithm:

- A bucket holds up to `capacity` tokens
- Tokens refill at `refill_rate` tokens per second
- Each request consumes 1 token (or more for batch operations)
- If no tokens remain, the request is rejected

### Why token bucket

- **Smooth traffic**: allows bursts up to capacity, then throttles
- **Predictable**: refill rate is constant
- **Fair**: all clients follow the same rule
- **Efficient**: O(1) per request, no queue needed (unlike leaky bucket)

### Implementation details

- Store current token count and last refill time
- On each request, compute elapsed time and issue new tokens: `new_tokens = min(capacity, current + elapsed_seconds * refill_rate)`
- Check if tokens >= requested; if yes, deduct and allow; otherwise reject

### Real-world use

Rate limiting is critical in production APIs:

- API gateways (AWS, Cloudflare) use token bucket to protect backends
- Message queues (RabbitMQ, Kafka) limit producer throughput
- CDNs use it to manage edge cache bandwidth

## Explanation

The solution maintains `current_tokens` and `last_refill_time`. On each `is_allowed()` call, compute how many tokens have been issued since the last refill, clamp to the capacity, deduct the requested amount, and return True/False. The key insight is that refill is lazy: we don't use a background timer; we compute available tokens on-demand when a request arrives.
