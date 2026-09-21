---
name: agentic-loop-minimal-react
title: 'A Minimal ReAct Loop: Thought -> Action -> Observation'
tags: [agentic-systems, agent-loop, orchestration]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every "agent" that does more than answer one question in one shot is running some version of the same tiny loop: the model reasons about what to do next (a _thought_), decides on a concrete _action_ to take, and gets back an _observation_ — the real-world result of that action — which feeds into its next thought. Repeat until the model decides it has enough to answer. This loop, ReAct (Reason + Act), is the base pattern underneath almost every agent framework; everything more sophisticated (retries, routing, multi-agent handoffs) is a variation layered on top of this same three-part cycle.

### From theory to code

You're given the model's full scripted sequence of `(thought, action, action_input)` turns — as if already generated, no real model call needed here — and a lookup table of what each action call actually returns. Implement `run_react_loop(steps, observations, max_steps)`. Process `steps` in order, up to `max_steps`. For each step, look up its observation from `observations` (using `"NO_OBSERVATION_FOUND"` if that exact `(action, action_input)` was never scripted), and append `(thought, action, action_input, observation)` to the trace. The moment `action == "finish"`, stop immediately — record that step with an empty observation and don't consult `observations` at all for it.

Return the trace built so far.

### Constraints

- 1 to 50 steps in the log; `max_steps >= 1`.
- `action` is never the literal string `"finish"` except to signal the loop should stop.

### Hints

<details>
<summary>Hint 1</summary>

Check the step budget _before_ processing each step, not after — that's what makes `max_steps` an exact cap on how many entries the returned trace can have, rather than an off-by-one over- or under-count.

</details>

<details>
<summary>Hint 2</summary>

The `"finish"` check has to come before the observation lookup, not after. If a `"finish"` entry accidentally has an entry in `observations` too, it must still never be consulted — finishing is a different kind of action, not just another tool call.

</details>

## Theory

### The simple version

Three moving parts, repeated: think, act, observe. The loop is a straight walk through a script that already exists (in a real system, the model generates each next step live, informed by the previous observation — but the _shape_ of the loop is identical either way), stopping at a specific terminal signal or a hard step ceiling, whichever comes first.

### Why "finish" is special, not just another action

Every other action in this loop expects a real observation back — that's the whole point of the cycle, feeding real-world results back into reasoning. `"finish"` isn't a request for information at all; it's the model declaring it's done reasoning and ready to answer. Treating it as a normal action needing a lookup would be a category error — there's nothing to observe, because nothing external was asked to happen.

### How this shows up in real systems

This exact three-field cycle (thought, action, observation) is the literal on-the-wire format many production agent frameworks use — it's not a simplification for teaching purposes, it's genuinely how the loop is implemented. Every other question in this track adds exactly one more piece of realism on top of this same shape: a budget, a decomposition step, a self-check, a repetition guard.

## Explanation

The function walks `steps` with an explicit index so the step-budget check can happen before any work for that step is done — the moment the index reaches `max_steps`, the loop stops without adding a partial entry. For each step still within budget, `action == "finish"` is checked first and short-circuits straight to appending a trace entry with an empty observation and breaking out of the loop, before `observations` is ever touched. Only a non-finish action reaches the `observations.get(...)` lookup, using the exact `(action, action_input)` pair as the key and falling back to the explicit `"NO_OBSERVATION_FOUND"` sentinel rather than silently defaulting to an empty string, which would be indistinguishable from a tool that legitimately returned nothing.
