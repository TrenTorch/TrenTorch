---
name: rl-alignment-value-iteration-mdp
title: Value Iteration on a Small Markov Decision Process
tags: [reinforcement-learning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every technique in this section — RLHF, PPO, DPO, reward modeling — is built on top of one foundational idea from classical reinforcement learning: given an environment where taking an action in a state leads (possibly randomly) to a new state and a reward, what's the best possible long-term strategy? Value iteration answers this exactly, for small enough environments, by repeatedly applying one simple update until it provably converges to the true optimal answer.

### From theory to code

Implement `bellman_backup` (one update step), `value_iteration` (repeat it to convergence), and `policy_evaluation_exact` (an independent, closed-form check on the result), for a Markov Decision Process described by transition probabilities `P` and rewards `R`.

### Constraints

- `P` has shape `(num_states, num_actions, num_states)`: `P[s, a, s']` is the probability of landing in `s'` after taking action `a` in state `s`. `R` has the same shape, giving the reward for that specific transition.
- `bellman_backup(V, P, R, gamma)` returns `(new_V, Q)`, where `Q[s, a] = sum_{s'} P[s, a, s'] * (R[s, a, s'] + gamma * V[s'])` and `new_V[s] = max_a Q[s, a]`.
- `value_iteration` repeats `bellman_backup` starting from `V = 0` until the largest per-state change drops below `theta`, then returns `(V, policy)` with `policy[s] = argmax_a Q[s, a]` from the final backup.
- `policy_evaluation_exact(policy, P, R, gamma)` solves `V = (I - gamma * P_pi)^-1 @ R_pi` directly via `np.linalg.solve`, where `P_pi`/`R_pi` restrict `P`/`R` to the actions `policy` actually takes.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`Q[s, a] = np.sum(P[s, a] * (R[s, a] + gamma * V))` works directly as vectorized NumPy — `P[s, a]` and `R[s, a]` are both length-`num_states` vectors, and `V` is too, so the whole sum-over-`s'` collapses into one line per `(s, a)` pair.

</details>

<details>
<summary>Hint 2</summary>

`value_iteration`'s stopping condition is `np.max(np.abs(new_V - V)) < theta` — once no state's value estimate is changing by more than `theta`, you've essentially found the fixed point of the Bellman optimality equation.

</details>

## Theory

### The simple version

Imagine a board game where every square has some possible moves, each move might randomly land you on a different square and pay out some coins, and you want to know the best possible total (discounted) coins you could earn starting from any given square, playing optimally forever. Value iteration finds this by guessing "the value of every square is 0", then repeatedly asking "given my CURRENT guess of every square's value, what's the best one-move choice from here, and how much is that worth?" — and just doing that over and over, the guesses providably converge to the true optimal values.

### The formula

```text
Bellman optimality equation (what value_iteration converges to):
    V*(s) = max_a sum_{s'} P(s'|s,a) * [R(s,a,s') + gamma * V*(s')]

One backup step:
    Q(s, a) = sum_{s'} P(s'|s,a) * [R(s,a,s') + gamma * V(s')]
    new_V(s) = max_a Q(s, a)

Exact policy evaluation (independent check), solving a linear system directly:
    V_pi = (I - gamma * P_pi)^-1 @ R_pi
```

`gamma` (the discount factor) controls how much future rewards matter relative to immediate ones — `gamma` close to `0` makes the agent short-sighted (only the very next reward matters), while `gamma` close to `1` makes it value long-term payoff almost as much as immediate reward, exactly as this exercise's `tests.py` demonstrates by comparing `gamma=0.1` against `gamma=0.99` on the same MDP.

### How PyTorch actually implements this

Context only, untested by your submission: value iteration itself predates deep learning entirely (Bellman, 1957) and is normally solved with plain dynamic programming, not neural networks or PyTorch — it only works when the state space is small enough to enumerate, which real-world RL (and everything downstream in this section, from PPO to DPO) exists specifically to work around, by learning approximate value/policy functions instead of computing them exactly.

## Explanation

`bellman_backup` computes every state-action pair's `Q`-value directly from the current value estimate `V`, then takes the max over actions to produce the improved value estimate for each state — one full sweep of dynamic programming.

`value_iteration` repeats this sweep, starting from an all-zero value estimate, until consecutive sweeps stop changing any state's value by more than `theta` — a provably convergent process for any MDP with `gamma < 1`, and the policy extracted from the final `Q` (greedily picking the best action per state) is provably the optimal policy.

`policy_evaluation_exact` provides a genuinely independent correctness check: rather than trusting that iteration converged to the right answer, it directly solves the linear system that defines the _true_ value of following `value_iteration`'s extracted policy forever, and this exercise's `tests.py` confirms the two methods agree — a real fixed-point verification, not just a self-consistency check between two copies of the same iterative logic.
