---
name: agentic-state-idempotent-execution
title: Idempotent Tool Execution Across Retries
tags: [agentic-systems, agent-state, reliability]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Retrying a failed tool call is usually safe — but not always. If a "charge the customer" call actually succeeded on the server side and only the *response* got lost (a network blip), blindly retrying it charges the customer twice. The standard fix is an idempotency key: every logical call gets a stable key, and the runtime only ever actually executes the call the first time a given key is seen — every later retry with the same key reuses whatever the first attempt already did, rather than doing it again.

### From theory to code

You're given the idempotency key for every attempted call, in order (a retry of the same logical call reuses the same key). Implement `dedupe_idempotent_calls(call_ids)`. For each call, decide whether it should actually **execute** (`True`, the first time this exact key is seen) or be treated as a no-op that reuses the earlier result (`False`, every later occurrence of an already-seen key). Return `(call_id, executed)` pairs, in the original order.

### Constraints

- 0 to 1000 calls; the same key may repeat any number of times, anywhere in the log.

### Hints

<details>
<summary>Hint 1</summary>

One `set` of keys already seen is the entire piece of state you need. A key executes iff it isn't already in that set — check first, then add it to the set either way (adding an already-present key to a set is a harmless no-op).

</details>

<details>
<summary>Hint 2</summary>

The two occurrences don't need to be adjacent — a retry of the same key can happen after any number of other, different calls in between. Membership in the seen-set is what matters, not position in the log.

</details>

## Theory

### The simple version

Walk the log once, keeping a running set of keys already seen. The first time a key shows up, it executes for real and gets added to the set. Every later time that exact same key shows up, it's a duplicate — skip execution, since whatever the first attempt did already stands.

### Why this is "idempotent," not just "deduplicated"

Idempotency is specifically about the *effect* of doing something twice being the same as doing it once — deduplication is the mechanism that achieves that here, but the underlying assumption is that the caller (or the original tool call) has already assigned a stable key that uniquely identifies *this specific logical operation*, distinct from any other call to the same tool. Given that assumption, "skip if already seen" is sufficient to guarantee the operation's real-world effect only happens once, no matter how many times a network retry re-sends the same request.

### How this shows up in real systems

Idempotency keys are a standard feature of payment APIs and any other API where a duplicate call has a real, unwanted side effect — the client generates a key once per logical operation, includes it on every retry of that same operation, and the server (or, here, the agent's own tool-execution layer) is responsible for recognizing a repeated key and short-circuiting to "already handled" instead of executing again.

## Explanation

The function keeps one `set`, `seen`, and walks `call_ids` once. For each call, `executed = call_id not in seen` captures the entire decision — true only the first time this key appears — computed *before* the key is added to the set, which is what correctly makes the first occurrence itself register as executed rather than being confused with a duplicate. The key is then added to `seen` unconditionally (a no-op if it was already there), and the `(call_id, executed)` pair is appended in the same order the calls were originally given, so the returned list is a direct parallel annotation of the input log rather than a reordering or filtering of it.
