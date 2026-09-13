---
name: production-ml-canary-deployment
title: 'Canary Deployment: Rolling a New Model Out to a Small Slice of Traffic First'
tags: [mlops]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`03-ci-cd-for-ml`'s test suite can only catch problems that were anticipated ahead of time — real production traffic often surfaces issues no test suite predicted. Canary deployment is the safety net: route only a small, controlled percentage of REAL traffic to the new model, leaving the rest on the trusted stable version, so a problem shows up affecting a small fraction of users instead of everyone at once.

### From theory to code

Implement `hash_bucket` (deterministic, uniformly-spread bucketing), `is_routed_to_canary` (the percentage-based routing decision), and `route_request`, tying the decision to an actual dispatch.

### Constraints

- `hash_bucket(key, num_buckets)` returns a deterministic bucket in `[0, num_buckets)`, based on a real cryptographic hash of `key`.
- `is_routed_to_canary(request_id, canary_percentage)` uses 100 buckets: routes to the canary exactly when the request's bucket is less than `canary_percentage`.
- The SAME `request_id` must ALWAYS route the same way, at a given `canary_percentage` — never a coin flip re-decided per call.
- `route_request` dispatches to whichever model function `is_routed_to_canary` selects.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

A cryptographic hash's output is effectively uniformly distributed across its whole range — reducing it modulo `num_buckets` spreads keys evenly across buckets, which is exactly what makes a hash-based router behave statistically like a real percentage split, without needing any actual randomness.

</details>

<details>
<summary>Hint 2</summary>

Using a REAL random number generator per-request (e.g. `random.random() < percentage/100`) would give the SAME request a DIFFERENT routing decision on a retry — a hash of the request's own ID is what makes routing decisions sticky and reproducible.

</details>

## Theory

### The simple version

Imagine a restaurant testing a new recipe by secretly serving it to whichever tables happen to be seated at a specific, fixed set of table NUMBERS (say, tables ending in the digit 7) rather than flipping a coin for every single order — a customer who sits at table 7 gets the new recipe every time they visit that table, consistently, which makes it much easier to track "how did table-7 customers react?" over repeated visits, compared to a purely random assignment that could put the same customer on either recipe on different nights.

### The formula

```text
hash_bucket(key, num_buckets) = int(sha256(key).hexdigest(), 16) % num_buckets

is_routed_to_canary(request_id, canary_percentage) = hash_bucket(request_id, 100) < canary_percentage

route_request(request_id, canary_percentage, canary_fn, stable_fn):
    canary_fn(request_id) if is_routed_to_canary(...) else stable_fn(request_id)
```

`canary_percentage=100` should route everything to the canary and `canary_percentage=0` should route nothing there — this exercise's `tests.py` confirms both boundary cases directly, alongside confirming that across MANY different request IDs, roughly the requested percentage actually lands in the canary bucket (a real statistical property of hashing, not a fabricated guarantee).

### How PyTorch actually implements this

Context only, untested by your submission: this hash-based, sticky routing scheme is exactly what real service meshes and load balancers (Istio, Envoy) implement for canary rollouts — deterministic hashing on a stable request attribute (a user ID, a session cookie) ensures the same user consistently sees the same version of a service across their whole session, rather than potentially bouncing between old and new behavior mid-session.

## Explanation

`hash_bucket` hashes a string key with SHA-256 and reduces it modulo the bucket count — `tests.py` confirms it's deterministic (same key, same bucket, every call) and always lands within the valid range.

`is_routed_to_canary` applies the percentage threshold directly against a 100-bucket hash — `tests.py` confirms the two boundary cases (0% and 100%) behave exactly as expected, that a mid-range percentage produces roughly the right SPLIT across thousands of distinct request IDs, and — via its final oracle test — that the decision is genuinely a deterministic FUNCTION of the request ID rather than incorporating any real randomness, since two independent passes over the same set of IDs must produce identical routing decisions.

`route_request` is the thin dispatch layer connecting the routing decision to an actual model call, letting the rest of a serving system stay agnostic to which specific model handled any given request.
