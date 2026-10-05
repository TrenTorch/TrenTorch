---
title: Upper Confidence Bound (UCB) Action Selection
name: rl-ucb-action-selection
difficulty: Intermediate
tags: [rl, bandits, exploration, confidence-bounds]
---

## Statement

Upper Confidence Bound is a principled exploration strategy that selects actions based on an optimistic estimate of their value, balancing exploitation and uncertainty-driven exploration.

### The problem, from first principles

In UCB, each action has an estimated value Q(a) and an uncertainty measure based on how many times it's been tried. The intuition: "if I'm unsure about an action, it might be the best—let me try it." Formally:

A_t = argmax_a [ Q(a) + c·sqrt(ln(t) / N(a)) ]

where:

- Q(a): average reward of action a
- N(a): times action a has been selected
- t: total time steps elapsed
- c: exploration constant

The second term is the confidence bonus. Actions with high uncertainty (low N(a)) or early in learning (high t initially) get larger bonuses.

### From theory to code

Implement `select_ucb_action(q_values, counts, t, c)` which:

- Takes action values Q(a) for each action
- Takes visit counts N(a) for each action
- Takes the current time step t (≥ 1)
- Takes exploration constant c > 0
- Returns the selected action index

Select the action with the highest upper confidence bound.

### Constraints

- q_values and counts have the same length (≥ 1)
- counts[a] ≥ 0, with at least one action having count > 0
- t ≥ 1
- c > 0 (typically 1 or sqrt(2))
- Handle the case where an action has never been tried (count=0): the UCB is +∞, so always pick it

### Hints

<details>
<summary>Hint 1: Confidence bonus formula</summary>
bonus[a] = c * sqrt(ln(t) / N(a))

But if N(a) = 0, return np.inf.
</details>

<details>
<summary>Hint 2: Handle zero counts</summary>
Use np.where or a loop to avoid division by zero.
</details>

<details>
<summary>Hint 3: Compute UCB for all actions</summary>
ucb = q_values + bonus, then argmax.
</details>

## Theory

### The simple version

Action A: Q(A)=5, N(A)=10. Action B: Q(B)=4.5, N(B)=100. At t=1000, c=1:

UCB(A) = 5 + 1·sqrt(ln(1000)/10) ≈ 5 + 1.72 = 6.72
UCB(B) = 4.5 + 1·sqrt(ln(1000)/100) ≈ 4.5 + 0.54 = 5.04

Despite lower average reward, A is selected because it's been tried less and might be better.

### The formula

UCB(a) = Q(a) + c·sqrt(ln(t) / N(a))

The bonus term:

- Grows with time (ln(t) increases)
- Shrinks as you sample an action (N(a) increases)
- Controlled by exploration constant c

### Optimality

Under certain conditions (i.i.d. rewards), UCB-style algorithms achieve logarithmic regret: the best possible bound in expectation. This is much better than epsilon-greedy, which has linear regret.

### Why it works

New actions always have low N(a), so they get large bonuses, ensuring exploration. But as an action is tried and its Q-value drops (or stays low), both the bonus shrinks and the value term is low, so it's eventually abandoned. Conversely, actions with high Q are also tried more (high bonus for high Q), so exploitation is automatic.

## Explanation

UCB is theoretically elegant but computationally simple. It requires only:

- The average reward (Q(a))
- The number of tries (N(a))
- The time step (t)

No random number generation, fully deterministic. This makes it reproducible and easier to analyze. In practice, it works as well as epsilon-greedy on many problems, and better on problems where you want automatic, principled exploration.

One downside: it's less stable with non-stationary rewards, since the logarithmic bonus assumes a fixed environment.
