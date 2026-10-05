---
title: Neural Network Approximation Layers
name: rl-nn-layers
difficulty: Advanced
tags: [rl, neural-networks, function-approximation, deep-learning]
---

## Statement

Deep value function: stack fully-connected layers with ReLU activations. Final layer outputs scalar V(s).

### The problem, from first principles

Linear approximation is limited. Neural networks learn nonlinear basis functions automatically. Deep networks can approximate complex value functions.

### From theory to code

Implement `forward_pass(state, weights, biases)` which:

- Takes state vector and network parameters
- Applies sequence of layers: linear -> ReLU -> ... -> linear (final)
- Returns scalar value estimate
- Weights list: W1, W2, ..., Wn
- Biases list: b1, b2, ..., bn

### Constraints

- All hidden layers use ReLU: max(0, x)
- Final layer has no activation (can be negative)
- Dimensions must match: state -> hidden -> ... -> 1

### Hints

<details>
<summary>Hint 1: Layer computation</summary>
h = relu(W @ state + b)
</details>

<details>
<summary>Hint 2: Chain of layers</summary>
Output of one layer is input to next
</details>

<details>
<summary>Hint 3: Final layer</summary>
No activation, outputs raw value
</details>

## Theory

### Multi-layer perceptron

V(s) = W_n * relu(W_{n-1} * ... * relu(W_1 * s + b_1) ... + b_{n-1}) + b_n

### Universal approximation

Deep networks can approximate any Borel-measurable function (universal approximation theorem).

## Explanation

Deep RL uses deep networks for value and policy. Classic architecture: two or three hidden layers of 64-256 units.
