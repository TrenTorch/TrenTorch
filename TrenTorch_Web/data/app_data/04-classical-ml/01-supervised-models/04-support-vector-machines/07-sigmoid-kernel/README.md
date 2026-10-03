---
name: support-vector-machines-sigmoid-kernel
title: Sigmoid kernel
tags: [classic-ml]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`Linear kernel` and `Polynomial kernel` both grow without bound as inputs grow. The sigmoid kernel squashes its output through a `tanh`, so every similarity lands strictly between `-1` and `1`. It resembles the activation of a single neural network neuron applied to a dot product, which is why it appears in SVM libraries as the kernel closest to a two-layer network.

Given `X` with shape `(n, d)` and `Y` with shape `(m, d)`, return the `(n, m)` matrix of sigmoid similarities.

### Constraints

- Return an array of shape `(n, m)` where entry `[i, j]` equals `tanh(gamma * X[i] @ Y[j] + coef0)`.
- Defaults: `gamma=1.0`, `coef0=0.0`.
- Build it on top of `linear_kernel` from the earlier question, which is already available to load.
- Do not modify `X` or `Y`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

This is the polynomial kernel's pattern with the power replaced by `tanh`.

</details>

<details>
<summary>Hint 2</summary>

`np.tanh` works elementwise on a whole array, so no loop is needed.

</details>

## Theory

### The simple version

Take the dot product, scale it, shift it, and then squeeze it into the range from `-1` to `1` with `tanh`. Large positive alignment saturates near `1`, large negative alignment saturates near `-1`, and points near the middle keep a roughly linear response.

### The formula

$$
k_{\text{sig}}(x, y) = \tanh\left(\gamma\, x^\top y + c\right)
$$

where $c$ is `coef0`. The kernel is symmetric in its arguments, and with $\gamma = 1$ and $c = 0$ it is $\tanh(x^\top y)$.

## Explanation

`sigmoid_kernel` loads `linear_kernel` from its own question, multiplies by `gamma`, adds `coef0`, and applies `np.tanh` elementwise. The `tanh` is the only nonlinearity, which is what keeps the output inside the open interval from `-1` to `1`.
