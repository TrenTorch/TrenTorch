---
name: research-lookahead-trajectory
title: 'Lookahead: The Slow Trajectory'
tags: [research-papers, optimization, meta-optimizer]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Across many synchronizations the slow weight behaves like an exponential moving average of the fast weights. Each sync pulls it toward the latest fast point, and the pull carries forward.

### From theory to code

Implement `slow_trajectory(phi0, fast_points, alpha)`, the sequence of slow weights over the syncs.

### Constraints

- Carry the slow weight forward between syncs.

### Hints

<details>
<summary>Hint 1</summary>

Loop over the fast points, applying the sync update to the running slow value, and record it.

</details>

## Theory

### The simple version

The slow trajectory is an exponential moving average, so it smooths the noise of the fast weights across syncs.

### The formula

$$\phi_{n} = \phi_{n-1} + \alpha(\theta_n - \phi_{n-1})$$

### How NumPy/PyTorch actually implements this

Lookahead implementations store the slow copy and update it at each sync.

## Explanation

Hand case: first sync gives 0.5, second gives 0.5 + 0.5 * 0.5 = 0.75.
