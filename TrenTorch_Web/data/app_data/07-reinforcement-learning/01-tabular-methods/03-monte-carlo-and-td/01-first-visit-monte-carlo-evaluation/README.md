---
name: monte-carlo-and-td-first-visit-monte-carlo-evaluation
title: First-visit Monte Carlo policy evaluation
tags: [reinforcement-learning, monte-carlo, policy-evaluation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Value iteration needs a model of the environment. Monte Carlo evaluation needs none: just run complete episodes, and for each state average the total discounted reward that followed its visits.

### From theory to code

Implement `first_visit_mc(episodes, gamma)`. Each episode is a list of `(state, reward)` pairs, where `reward` is received on leaving that state. For every state, average the discounted return that followed its *first* visit in each episode.

### Constraints

- `episodes` is a list of episodes; an episode is a list of `(state, reward)` tuples in time order. States are hashable.
- `gamma` is the discount factor in `[0, 1]`.
- The return at step `t` is `reward_t + gamma * return_{t+1}`, with the return after the last step being 0.
- Return a `dict` mapping each visited state to a Python `float`. A state's value averages one return per episode that visits it.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Compute returns for an episode by sweeping backwards: `G = reward + gamma * G`.

</details>

<details><summary>Hint 2</summary>

Walk the episode forward and record a return only the first time each state appears.

</details>

## Theory

### The simple version

Play the game many times. Each time you land in a state, note how much reward you collected from then on. The state's value is the average of those notes. 'First visit' means that if you land in the same state twice in one episode, only the earlier landing counts.

### The formula

$$G_t = r_t + \gamma\, G_{t+1}, \quad G_T = 0, \qquad V(s) = \frac{1}{N(s)} \sum_{\text{episodes}} G_{t_{\text{first}}(s)}$$

### How libraries implement this

Sutton & Barto, chapter 5. Every-visit Monte Carlo averages the return at all visits instead; both converge to the true value, with different bias and variance.

## Explanation

Computing all returns in one backward pass is linear in the episode length. A `seen` set per episode enforces the first-visit rule, and a dict of lists of returns keeps the final average a simple mean.
