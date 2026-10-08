---
name: research-act-output
title: 'Adaptive Computation Time: The Weighted Output'
tags: [research-papers, sequence-models, adaptive-computation, recurrence]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The ACT output is a weighted average of the states after each step, where the weights are the halting probabilities and the last step takes the remainder. The output is differentiable with respect to the halting decision.

### From theory to code

Implement `act_output(outs, halts)`, the halting-weighted output.

### Constraints

- Weights sum to one.

### Hints

<details>
<summary>Hint 1</summary>

Use the halting probabilities for all steps but the last, give the last step the remainder, and take the weighted sum.

</details>

## Theory

### The simple version

Weighting by halting probabilities lets gradients reach the halting unit, so the network learns when to stop without a discrete decision.

### The formula

$$y = \sum_{t=1}^{N} p_t\,y_t, \qquad p_N = R$$

### How NumPy/PyTorch actually implements this

ACT models compute this blend of intermediate states at each position.

## Explanation

The weights are a probability distribution over steps by construction, so the output is a proper average.
