---
name: agentic-orchestration-message-passing-shared-state
title: Message-Passing Between Two Agents Over Shared State
tags: [agentic-systems, multi-agent, orchestration]
difficulty: Beginner
---

## Statement

### The problem, from first principles

One common way for multiple agents to coordinate without a rigid supervisor hierarchy is a shared blackboard: any agent can write a value under a named key, and any agent can read the current value of any key. There's no negotiation protocol, no locking — just a simple rule for what happens when two agents write the same key: whoever wrote most recently wins, and the system remembers who that was.

### From theory to code

You're given the full message log: `(sender, key, value)` triples, in order, where each message writes `value` into the shared state under `key`. Implement `process_message_log(messages)`. Process the messages in order. Return the final state: a dict from key to `(value, last_writer)`, reflecting whichever message most recently wrote that key.

### Constraints

- 0 to 1000 messages; any number of distinct agents and keys.

### Hints

<details>
<summary>Hint 1</summary>

One dict, updated in a single forward pass, is the entire solution — for each message, just overwrite `state[key]` with the new `(value, sender)` pair. There's no need to check whether the key already exists; overwriting unconditionally already implements "last write wins."

</details>

<details>
<summary>Hint 2</summary>

The same agent overwriting its own earlier write to the same key is not a special case — it's handled by the exact same unconditional overwrite as two different agents writing the same key.

</details>

## Theory

### The simple version

A shared blackboard is just a dict that gets built up by walking the message log once, in order, and unconditionally overwriting whatever's currently at each message's key. There's nothing more to the coordination protocol than that — no merge logic, no conflict resolution beyond "most recent wins."

### Why remember who wrote it, not just the value

Knowing only the current value of a shared key tells you *what* the agents currently agree on, but not *why* — if the value looks wrong, knowing which agent's write produced it is what lets you trace the problem back to a specific agent's behavior rather than treating the shared state as an opaque, unexplained blob. This is a small amount of extra bookkeeping that makes a shared-state system meaningfully more debuggable.

### How this shows up in real systems

The blackboard pattern is one of the oldest and simplest coordination mechanisms for multi-agent systems — no message needs to be addressed to a specific recipient, agents just publish to and read from shared keys, and the system doesn't need a central router deciding who talks to whom. Its simplicity is also its biggest limitation: with no locking or transactional guarantees, it only works safely when writes don't need to be atomic across multiple keys at once — a limitation worth understanding, not just the mechanic itself.

## Explanation

The function keeps one dict, `state`, and walks `messages` once in order, overwriting `state[key] = (value, sender)` on every message with no conditional logic at all — this single unconditional overwrite is exactly what "last write wins" means, since whichever message for a given key was processed most recently is, by construction, the one still sitting in the dict once the loop finishes. Different keys never interact with each other in this process, since each overwrite only ever touches the one key named in that specific message.
