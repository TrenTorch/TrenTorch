---
name: agentic-step-efficiency-redundancy
title: Step Efficiency & Redundancy
tags: [agentic-systems, evaluation, efficiency, trajectories]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Two agents can both solve a task, but one in 4 steps and the other in 40, repeating searches, re-reading the same file and retrying a failing command unchanged. The slow agent costs ten times more, takes ten times longer and is more likely to wander off. Evaluation therefore measures not only **whether** a task succeeded but **how efficiently**. **Step efficiency** compares the number of steps taken with the minimum known for the task (and is zero if the task failed, since an efficient failure is not a virtue). **Redundancy** counts actions that exactly repeat an earlier action, the signature of a stuck loop.

### From theory to code

Implement `step_efficiency` and `redundancy_rate`.

### Constraints

- `step_efficiency(n_steps, n_optimal, succeeded)` returns `0.0` if `succeeded` is false, else `min(1.0, n_optimal / n_steps)`. `n_steps >= 1`.
- `redundancy_rate(actions)` takes a list of `(name, args)` pairs (args is a dict) and returns the fraction of actions that **exactly repeat** an earlier action (same name and equal args). Return `0.0` for an empty list.
- Key actions with `(name, json.dumps(args, sort_keys=True))`.

### Hints

<details>
<summary>Hint 1</summary>

The first occurrence of an action is never redundant, only later copies.

</details>

<details>
<summary>Hint 2</summary>

An agent can beat the recorded optimum (`n_steps < n_optimal`), which the cap at 1.0 handles.

</details>

## Theory

### The simple version

Judging two couriers: both deliver the parcel, but one drove straight there and the other circled the block four times. The ratio of minimum to actual distance is the efficiency, and the circles are the redundancy.

### The formula

$$
\text{eff} = \mathbf{1}[\text{success}]\cdot\min\Big(1, \frac{n^\ast}{n}\Big), \qquad \text{redundancy} = \frac{\big|\{ i : a_i \in \{a_1, \dots, a_{i-1}\}\}\big|}{n}
$$

### How this is done in practice

Agent benchmarks report steps, tool calls, tokens and cost per task next to success. High redundancy is a cheap loop detector in production, and the loop-detection questions earlier in this track act on the same signal at run time.

## Explanation

The two metrics are deliberately simple and complementary: efficiency compares to a reference, redundancy needs no reference at all.
