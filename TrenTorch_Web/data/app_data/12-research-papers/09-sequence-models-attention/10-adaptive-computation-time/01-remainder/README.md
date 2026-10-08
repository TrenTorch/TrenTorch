---
name: research-act-remainder
title: 'Adaptive Computation Time: The Remainder'
tags: [research-papers, sequence-models, adaptive-computation, recurrence]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Adaptive Computation Time (Graves, 2016) lets a recurrent network decide how many steps to think before answering. At each step it accumulates a halting probability, and the last step gets the remainder so the weights sum to one.

### From theory to code

Implement `act_remainder(halts)`, the weight left for the final step.

### Constraints

- The remainder makes the step weights sum to one.

### Hints

<details>
<summary>Hint 1</summary>

Subtract the probabilities of all steps except the last from one.

</details>

## Theory

### The simple version

The remainder guarantees that the output is a proper weighted average over the steps the network took, so the halting decision stays differentiable.

### The formula

$$R = 1 - \sum_{t=1}^{N-1} p_t$$

### How NumPy/PyTorch actually implements this

ACT implementations track the cumulative halting sum in a loop and stop when it passes one minus epsilon.

## Explanation

Earlier halting probabilities accumulate, and the remainder is what the final step contributes.
