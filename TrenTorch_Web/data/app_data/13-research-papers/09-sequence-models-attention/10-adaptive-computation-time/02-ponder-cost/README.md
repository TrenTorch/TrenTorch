---
name: research-act-ponder-cost
title: 'Adaptive Computation Time: The Ponder Cost'
tags: [research-papers, sequence-models, adaptive-computation, recurrence]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Without a penalty, ACT would think for as long as possible. The ponder cost adds a small price per step, so the network thinks only as long as the extra computation helps.

### From theory to code

Implement `act_ponder_cost(n_steps, tau)`, the penalty added to the training loss.

### Constraints

- Returns a float.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the step count by the penalty weight.

</details>

## Theory

### The simple version

The penalty trades accuracy against computation. Tuning tau sets how much compute the model spends per input.

### The formula

$$\mathcal{L}_{\text{ponder}} = \tau\,N$$

### How NumPy/PyTorch actually implements this

Adaptive-depth models add this term to their objective in the same linear form.

## Explanation

The paper adds this cost to the task loss and reports the average number of steps per example.
