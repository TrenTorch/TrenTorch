---
name: research-sgdr-cycle-position
title: 'SGDR: Finding the Cycle Position'
tags: [research-papers, optimization, learning-rate-schedule, restarts]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

With warm restarts the cycle length grows by a fixed multiplier after each restart. Locating a global step means subtracting whole cycles and tracking the current cycle length.

### From theory to code

Implement `sgdr_position(t, T0, Tmult)`, returning the position in the current cycle and its length.

### Constraints

- Restarts happen at the start of each cycle.

### Hints

<details>
<summary>Hint 1</summary>

Subtract the current cycle length from t while t is at least that length, growing the cycle length each time.

</details>

## Theory

### The simple version

Growing cycles give long low-rate phases late in training, when fine convergence matters most.

### The formula

$$T_i = T_0\,T_{\text{mult}}^{\,n}$$

### How NumPy/PyTorch actually implements this

Restart-schedule code keeps the same loop to map a global step onto the current cycle.

## Explanation

Hand case: with T0 = 10 and Tmult = 2, step 12 is 2 steps into the second cycle of length 20.
