---
name: research-lookahead-slow-sync
title: 'Lookahead: The Slow Weight Sync'
tags: [research-papers, optimization, meta-optimizer]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Lookahead (Zhang et al., 2019) wraps any inner optimizer. It keeps a slow copy of the weights, runs k fast steps, then moves the slow weights part of the way toward the result.

### From theory to code

Implement `lookahead_sync(slow, fast, alpha)`, the interpolation of slow weights toward fast ones.

### Constraints

- alpha is between 0 and 1.

### Hints

<details>
<summary>Hint 1</summary>

Add alpha times the difference between the fast and slow weights to the slow weights.

</details>

## Theory

### The simple version

The slow weights smooth out the noisy trajectory of the fast optimizer, which tends to help generalization without extra hyperparameter tuning.

### The formula

$$\phi \leftarrow \phi + \alpha(\theta - \phi)$$

### How NumPy/PyTorch actually implements this

Implementations keep a second copy of the parameters and run this update every k steps.

## Explanation

Alpha equal to one copies the fast weights, alpha zero ignores them; the tests check both ends.
