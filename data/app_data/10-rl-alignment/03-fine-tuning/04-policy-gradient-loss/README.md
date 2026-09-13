---
name: rl-alignment-policy-gradient-loss
title: Policy Gradient Loss
tags: [reinforcement-learning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`rl-alignment-tabular-q-learning` learned a Q-VALUE table directly, then acted greedily with respect to it. Policy gradient methods take a different route: train the POLICY (the action-selection strategy itself) directly via gradient ascent on expected return, using a beautifully simple update rule — "increase the log-probability of actions that led to good outcomes, decrease it for actions that led to bad ones." This question builds both pieces: the outcome signal (`discounted_returns`) and the loss that turns it into a gradient (`policy_gradient_loss`).

### From theory to code

Implement `discounted_returns` (the REINFORCE return at every timestep, computed efficiently via one backward pass, correctly resetting at episode boundaries) and `policy_gradient_loss` (the basic policy-gradient loss).

### Constraints

- `discounted_returns(rewards, gamma, dones)[t] = rewards[t] + gamma * (1 - dones[t]) * discounted_returns[t+1]`, with the sequence treated as ending after the last index.
- `dones[t] = 1` means episode `t` is the LAST step of an episode — the return computation must NOT carry any value across that boundary into the next episode.
- `policy_gradient_loss(log_probs, advantages)` returns `-mean(log_probs * advantages)`.
- Increasing `log_probs` for an action with a POSITIVE advantage must strictly decrease the loss (the correct gradient-ascent direction).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`discounted_returns` is computed BACKWARD, from the last timestep to the first, maintaining one running total: `running = rewards[t] + gamma * (1 - dones[t]) * running` — the `(1 - dones[t])` factor is what zeroes out the carry-over exactly at an episode boundary.

</details>

<details>
<summary>Hint 2</summary>

`policy_gradient_loss` doesn't need `discounted_returns` internally — it's a general-purpose function that works with ANY advantage-like signal, whether that's raw returns from this exercise, or GRPO's group-normalized advantage, or GAE's more sophisticated estimate (`rl-alignment-generalized-advantage-estimation`).

</details>

## Theory

### The simple version

Imagine an athlete reviewing footage of an entire game, working backward from the final score: for every single decision they made during the game, they figure out "given everything that happened AFTER this moment, how good was this specific decision, really?" — a decision followed by a great outcome gets a high score, one followed by a poor outcome gets a low score, and decisions from EARLIER in the game naturally accumulate credit from everything good (or bad) that followed. `discounted_returns` computes exactly this "credit assigned looking forward from each moment" signal, and `policy_gradient_loss` is simply "reinforce the decisions that earned high credit, discourage the ones that earned low credit."

### The formula

```text
discounted_returns(rewards, gamma, dones):
    running = 0
    for t from LAST index down to 0:
        running = rewards[t] + gamma * (1 - dones[t]) * running
        returns[t] = running

policy_gradient_loss(log_probs, advantages) = -mean(log_probs * advantages)
```

The loss's raw numeric VALUE at a given point isn't the interesting thing — what matters is its GRADIENT direction: for a positive advantage, this loss decreases as `log_prob` increases (correctly reinforcing that action), and for a negative advantage, it decreases as `log_prob` DEcreases (correctly discouraging it) — the exact same underlying idea GRPO's `grpo_policy_gradient_loss` already used, just paired here with plain discounted returns instead of a group-normalized advantage.

### How PyTorch actually implements this

Context only, untested by your submission: this is the REINFORCE algorithm (Williams, 1992), the foundational policy-gradient method that PPO (`rl-alignment-ppo-clipped-surrogate-objective`) and GRPO (`rl-alignment-grpo-group-relative-advantage`) both build on and improve — REINFORCE's known weakness is HIGH VARIANCE (raw returns can swing wildly between episodes), which is exactly the problem `rl-alignment-generalized-advantage-estimation`'s more sophisticated advantage estimate exists to reduce.

## Explanation

`discounted_returns` runs the standard backward recursive computation, resetting the accumulated running total to start fresh at every episode boundary — `tests.py` confirms the formula against hand computation, confirms `gamma=1` reduces to a plain reverse cumulative sum, and — via its final oracle test — confirms a multi-episode reward sequence produces IDENTICAL early returns to what each episode would give computed completely independently, directly ruling out a mutant that ignores `dones` and lets rewards leak across episode boundaries.

`policy_gradient_loss` is the direct `-mean(log_prob * advantage)` computation — `tests.py` verifies the property that actually matters for training: for a fixed positive advantage, increasing `log_prob` genuinely lowers the loss, confirming this loss function points gradient descent in the correct, return-improving direction.
