---
name: rl-alignment-generalized-advantage-estimation
title: Generalized Advantage Estimation (Pairs With Policy Gradient)
tags: [reinforcement-learning]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`rl-alignment-policy-gradient-loss`'s raw discounted returns work, but they're noisy: a single episode's return depends on every random action taken throughout the WHOLE episode, so two runs of the exact same good policy can produce wildly different returns just from randomness elsewhere. GAE (Generalized Advantage Estimation) fixes this by blending many different "look-ahead lengths" of the TD residual into one smoothed advantage estimate, controlled by a single interpolation parameter, `lambda`.

### From theory to code

Implement `td_residuals` (the one-step prediction error a value function makes) and `generalized_advantage_estimation`, computing the full GAE via one efficient backward recursive pass.

### Constraints

- `td_residuals(rewards, values, next_values, dones, gamma)[t] = rewards[t] + gamma * next_values[t] * (1 - dones[t]) - values[t]`.
- `generalized_advantage_estimation(..., lam)[t] = td_residuals[t] + gamma * lam * (1 - dones[t]) * generalized_advantage_estimation[t+1]`, computed backward, with the value past the last index treated as `0`.
- `lam=0` must reduce EXACTLY to `td_residuals` itself.
- `lam=1` must reduce EXACTLY to the full Monte-Carlo advantage: `discounted_returns(rewards, gamma, dones) - values`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`generalized_advantage_estimation` is structurally identical to `rl-alignment-policy-gradient-loss`'s `discounted_returns` backward loop — same reset-at-`dones` pattern — except the thing being accumulated is `td_residuals` scaled by `gamma * lam` each step, instead of raw rewards scaled by `gamma` alone.

</details>

<details>
<summary>Hint 2</summary>

Verify your implementation against a completely different (much slower) brute-force approach: directly sum `sum_k (gamma*lam)^k * delta[t+k]` for every `t`, stopping at the next episode boundary — if the fast recursive version and this direct definition don't agree, something in the recursion is wrong.

</details>

## Theory

### The simple version

Imagine estimating how good a chess move was using several different amounts of "hindsight": look just ONE move ahead (very fast feedback, but noisy — a lot can still go wrong or right afterward), or wait for the ENTIRE rest of the game to finish before judging (very informative, but you have to wait a long time and the final result depends on a huge number of later, unrelated moves too). GAE doesn't pick just one of these — it blends together EVERY possible look-ahead length at once, weighted so that shorter look-aheads count more (controlled by `lambda`), giving an estimate that's less noisy than pure Monte-Carlo but less biased than a single-step estimate.

### The formula

```text
td_residuals(r, V, V', done, gamma)[t] = r[t] + gamma * V'[t] * (1 - done[t]) - V[t]

generalized_advantage_estimation(..., lam)[t] = delta[t] + gamma * lam * (1 - done[t]) * gae[t+1]
    (computed backward, gae[T] treated as 0)

Special cases:
    lam = 0  ->  gae == td_residuals                          (pure one-step TD)
    lam = 1  ->  gae == discounted_returns(r, gamma, done) - V  (pure Monte-Carlo advantage)
```

Every value of `lam` strictly between `0` and `1` interpolates between these two extremes — a genuinely useful knob, not just a mathematical curiosity, since it directly trades off estimator bias (favoring `lam` near `0`, which trusts the value function more) against estimator variance (favoring `lam` near `1`, which trusts the actual observed rewards more).

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact algorithm from "High-Dimensional Continuous Control Using Generalized Advantage Estimation" (Schulman et al., 2016), the advantage estimator PPO (`rl-alignment-ppo-clipped-surrogate-objective`) was originally paired with in its introducing paper — real implementations (Stable-Baselines3, TRL's `PPOTrainer`) compute exactly this backward recursive pass over a collected rollout buffer before running any policy-gradient update.

## Explanation

`td_residuals` computes the value function's one-step prediction error directly, with the `(1 - dones[t])` term correctly zeroing out the bootstrap term at an episode's true final step (where there's no valid next state to bootstrap from) — `tests.py` confirms this via a case with a deliberately huge, wrong `next_values` entry that must be ignored precisely because `dones` marks that step as terminal.

`generalized_advantage_estimation` runs the same kind of backward recursive accumulation `discounted_returns` used, but weighted by `gamma * lam` per step instead of `gamma` alone — `tests.py` verifies the result against a slow, independently-implemented brute-force summation of the GAE definition, confirms the two documented special cases (`lam=0` reduces to plain `td_residuals`, `lam=1` reduces to the full Monte-Carlo advantage) hold exactly, and — via its final oracle test — confirms two independent episodes concatenated together produce identical results to one combined multi-episode computation, directly ruling out a mutant that lets the recursive accumulator leak information across an episode boundary.
