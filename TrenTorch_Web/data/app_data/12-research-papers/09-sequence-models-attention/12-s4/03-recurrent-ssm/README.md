---
name: research-s4-recurrent-ssm
title: 'S4: The Recurrent Form'
tags: [research-papers, sequence-models, state-space, sequence]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The same system can be run as a recurrence, one step at a time, which is how S4 generates at inference. Both forms give identical outputs, so the convolution used in training is exact.

### From theory to code

Implement `recurrent_ssm(A_bar, B_bar, C, x)`, the step-by-step recurrence with output readout.

### Constraints

- It must match the convolution form exactly.

### Hints

<details>
<summary>Hint 1</summary>

Keep a state, update it with the input each step, then output C times the state.

</details>

## Theory

### The simple version

The recurrence is cheap for generation, and the convolution is fast for training. S4 gets both from one set of parameters.

### The formula

$$h_t = \bar A h_{t-1} + \bar B x_t,\qquad y_t = C h_t$$

### How NumPy/PyTorch actually implements this

S4 inference runs the recurrence with a constant-size state per generated token.

## Explanation

The equivalence between the two forms is what the first test verifies numerically.
