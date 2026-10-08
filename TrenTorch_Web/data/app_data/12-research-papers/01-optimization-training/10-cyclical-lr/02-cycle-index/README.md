---
name: research-clr-cycle-index
title: 'Cyclical Learning Rates: The Cycle Index'
tags: [research-papers, optimization, learning-rate-schedule]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Each full cycle of the triangular schedule spans two half-cycles. The cycle index tells the schedule which triangle it is on, and it sets where the peak falls.

### From theory to code

Implement `cycle_index(it, step)`, the 1-indexed cycle containing the iteration.

### Constraints

- Return an integer.

### Hints

<details>
<summary>Hint 1</summary>

Divide the iteration by twice the half-cycle length, add one, and take the floor.

</details>

## Theory

### The simple version

The cycle index is the cheapest piece of the schedule to get right; a wrong index shifts every peak.

### The formula

$$c = \left\lfloor 1 + \frac{t}{2s}\right\rfloor$$

### How NumPy/PyTorch actually implements this

Schedulers compute this index once per iteration before the triangle is evaluated.

## Explanation

Hand case: with step 4, iteration 10 is in cycle floor(1 + 1.25) = 2.
