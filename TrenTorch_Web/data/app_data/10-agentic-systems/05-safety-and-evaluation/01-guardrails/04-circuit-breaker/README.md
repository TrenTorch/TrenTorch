---
name: agentic-circuit-breaker
title: Circuit Breaker
tags: [agentic-systems, reliability, circuit-breaker, tools]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

When a tool or API is down, an agent that keeps calling it wastes time and money, and may hammer a service that is trying to recover. A **circuit breaker** wraps the calls and tracks failures. In the **closed** state calls pass through. After `failure_threshold` consecutive failures it **opens**: calls are rejected immediately without being attempted. After a `cooldown` period it moves to **half-open** and allows a single trial call. If the trial succeeds the circuit closes again, and if it fails the circuit reopens for another cooldown. For testability the class takes the current time as an argument instead of reading a clock.

### From theory to code

Implement the class `CircuitBreaker`.

### Constraints

- `CircuitBreaker(failure_threshold, cooldown)` starts closed with zero consecutive failures.
- `allow(now)` returns `True` if a call may be attempted. Closed: `True`. Open: `False` until `now - opened_at >= cooldown`, at which point the state becomes half-open and it returns `True`. Half-open: `True` only for the first call; while that trial is outstanding return `False`.
- `record_success(now)` resets the failure count and closes the circuit. `record_failure(now)`: in half-open state it reopens immediately with `opened_at = now`; in closed state it increments the failure count and opens (with `opened_at = now`) when the count reaches `failure_threshold`.
- `state` is an attribute holding `'closed'`, `'open'` or `'half_open'`.

### Hints

<details>
<summary>Hint 1</summary>

Track `failures`, `opened_at` and whether the half-open trial has been handed out.

</details>

<details>
<summary>Hint 2</summary>

A success in the closed state simply resets the counter, so only _consecutive_ failures count.

</details>

## Theory

### The simple version

A fuse in an electrical panel: after repeated overloads it trips so the house is protected, and an electrician later tries it once to see if the fault has cleared.

### The formula

$$
\text{closed} \xrightarrow{\ f \ge F\ } \text{open} \xrightarrow{\ \Delta t \ge T\ } \text{half-open} \xrightarrow{\text{success}} \text{closed}, \qquad \text{half-open} \xrightarrow{\text{failure}} \text{open}
$$

### How this is done in practice

Resilience libraries (Hystrix, Polly, `pybreaker`) implement this pattern, and it combines naturally with retries and backoff: retries handle brief glitches, the breaker handles sustained outages. For agents it also prevents a looping model from burning its budget on a dead tool.

## Explanation

The class is a three-state machine. The subtle part is half-open: exactly one probe is allowed, so concurrent callers do not all rush back to a service that may still be down.
