---
name: research-dqn-epsilon-schedule
title: 'DQN: Annealing Exploration'
tags: [research-papers, reinforcement-learning, deep-q-learning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Early in training the agent knows little, so it should explore often. DQN (Mnih et al., 2015) starts with a high exploration rate and decays it over the first million frames, then holds it low.

### From theory to code

Implement `epsilon_schedule(step, start, end, decay_steps)`, a linear decay from `start` to `end` that holds `end` afterward.

### Constraints

- `decay_steps` is positive.

### Hints

<details>
<summary>Hint 1</summary>

Interpolate with `step / decay_steps` as the fraction of progress, clamped once it reaches 1.

</details>

## Theory

### The simple version

Exploration is a resource that is most valuable early. A linear schedule is simple and gives the agent a predictable transition from exploring to exploiting.

### The formula

$$\epsilon_t = \begin{cases} \epsilon_s + (\epsilon_e - \epsilon_s)\,t / T & t < T \\ \epsilon_e & t \ge T \end{cases}$$

### How NumPy/PyTorch actually implements this

Training loops implement this with a `LinearSchedule` helper that returns the same value per step.

## Explanation

The schedule is the function of step that the epsilon-greedy policy reads before choosing each action.
