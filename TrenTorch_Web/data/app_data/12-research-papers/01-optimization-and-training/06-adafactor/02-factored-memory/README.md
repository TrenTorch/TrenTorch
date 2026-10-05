---
name: research-adafactor-factored-memory
title: 'Adafactor: Memory Saved by Factoring'
tags: [research-papers, optimization, memory]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A full second-moment matrix for an n by m weight stores n times m numbers. Adafactor stores one vector of length n and one of length m, which is far smaller for large layers.

### From theory to code

Implement `factored_memory(n, m)`, the number of stored entries for a factored second moment.

### Constraints

- Return an integer.

### Hints

<details>
<summary>Hint 1</summary>

Add the two dimensions together.

</details>

## Theory

### The simple version

For big transformer layers the saving is large, which is why Adafactor was used to train models that would not fit with Adam's full state.

### The formula

$$\text{memory}_{\text{factored}} = n + m \quad\text{vs}\quad nm$$

### How NumPy/PyTorch actually implements this

Optimizer state accounting in training frameworks uses this count to estimate memory use.

## Explanation

Hand case: a 4 by 8 matrix needs 12 stored numbers instead of 32.
