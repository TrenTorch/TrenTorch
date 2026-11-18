---
title: Model-Based Planning with Learned Models
name: rl-model-based-planning
difficulty: Advanced
tags: [rl, model-based, planning, world-models]
---

## Statement

Learn environment model: predict s_{t+1} from (s_t, a_t). Use model for planning: simulate trajectories, pick actions with highest simulated returns.

### The problem, from first principles

Sample efficiency: real rollouts are expensive. Learn a forward model and plan with it. Trade off: model error accumulates, but reduces real interactions.

### From theory to code

Implement `dyna_update(real_trajectory, model, planning_steps)` which:

- Uses real trajectory to update value function
- Uses learned model for planning updates
- Takes planning_steps imagined trajectories
- Returns improved value estimates

### Constraints

- Model learns from real data
- Planning uses model to generate imagined data
- Model error can cause suboptimal policies
- Balance real vs imagined data

### Hints

<details>
<summary>Hint 1: Model training</summary>
Learn model to minimize prediction error on real data
</details>

<details>
<summary>Hint 2: Planning</summary>
Simulate trajectories using model, apply RL to imagined transitions
</details>

<details>
<summary>Hint 3: Dyna</summary>
Integrate real and imagined updates in same learning loop
</details>

## Theory

### Dyna-Q algorithm

1. Execute action a, observe (s,a,r,s')
2. Update Q from real transition
3. Update model: predict[s,a] = s'
4. For N planning steps: sample (s,a) from history, compute r+γmax V(s'), update Q
5. Repeat

### Sample Efficiency

Planning amplifies sample efficiency: one real sample generates multiple value updates.

## Explanation

Model-based RL is hot again. AlphaGo used learned lookahead, MuZero scaled it to Atari.
