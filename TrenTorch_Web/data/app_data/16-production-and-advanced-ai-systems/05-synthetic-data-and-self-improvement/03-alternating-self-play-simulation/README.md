---
name: production-synthetic-data-alternating-self-play
title: Simulate an Alternating Self-Play Transcript
tags: [production-systems, synthetic-data, self-improvement]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Self-play generates training data by having two copies of a model (or two roles -- a proposer and a critic, a debater on each side) take turns interacting, with the resulting transcript itself becoming a new training example. Simulating this turn-taking correctly is the harness logic underneath any self-play data-generation pipeline.

### The task

Write `simulate_self_play(agent_a_moves, agent_b_moves, max_turns)`. Agents "A" and "B" alternate turns starting with A, each drawing from its own pre-scripted move list in order. Build the `(agent_name, move)` transcript for up to `max_turns` turns, stopping early the moment the agent whose turn it is has no move left.

## Theory

### The simple version

Turn parity decides whose move it is (even turns are A's, odd turns are B's), and each agent's move index advances only on its own turns, not every turn. The loop stops either at the turn cap or the moment an agent runs dry, whichever comes first.

### Why stop on the moving agent's own move count, not the total

If either agent's supply of moves runs out, continuing to hand it a turn produces nothing meaningful -- there's no move left for it to make. Checking each agent's own move index against its own list (rather than some shared or combined length) is what correctly ends the transcript exactly when the moving agent specifically has nothing left, regardless of how many moves the other agent might still have.

### How this shows up in real systems

This is the control loop behind any turn-based self-play data generation setup: two roles alternate, and the process naturally ends whichever way it ends first -- a fixed turn budget, or one side simply running out of things to say.

## Explanation

Turn parity (`turn % 2`) picks the acting agent and its move list; `turn // 2` gives that agent's own move index, since each agent only advances on every other overall turn. The loop breaks the instant that index would go out of bounds for the acting agent's move list, so a transcript never contains a turn the acting agent had no scripted move for.
