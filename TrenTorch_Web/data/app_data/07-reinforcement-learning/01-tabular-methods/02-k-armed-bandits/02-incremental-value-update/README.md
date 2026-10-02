---
name: k-armed-bandits-incremental-value-update
title: Incremental action-value update
tags: [reinforcement-learning, bandits, value-estimation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

To estimate an arm's value you could store every reward it ever gave and average them, but that needs ever-growing memory. The same average can be maintained with just the current estimate and a count.

### From theory to code

Implement `update_action_value(q_values, counts, action, reward)`. Increment the pulled arm's count and move its estimate toward the new reward by `1 / count` of the gap.

### Constraints

- `q_values` is a float array and `counts` an integer array, one entry per arm.
- Return new arrays `(q_values, counts)`; do not modify the inputs.
- Only the pulled arm changes.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Increase `counts[action]` first, so the first-ever reward uses a step size of exactly 1.

</details>

<details><summary>Hint 2</summary>

The update is `q += (reward - q) / n`.

</details>

## Theory

### The simple version

Each new reward nudges the estimate by a shrinking fraction of the surprise (reward minus current estimate). After n pulls the estimate is exactly the sample mean of those rewards.

### The formula

$$N(a) \leftarrow N(a) + 1, \qquad Q(a) \leftarrow Q(a) + \frac{1}{N(a)}\big(r - Q(a)\big)$$

### How libraries implement this

Sutton & Barto call this the incremental sample-average update; replacing `1 / N` with a constant `alpha` gives the form used for non-stationary problems and in Q-learning.

## Explanation

Copying the arrays first keeps the function free of side effects. The `1 / N` step size is what makes the estimate an exact running average rather than an exponentially weighted one.
