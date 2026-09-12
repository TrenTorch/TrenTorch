---
name: dl-core-leaky-relu
title: LeakyReLU fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Beginner
---

## Statement

Implement:

```python
def leaky_relu_forward(x, negative_slope=0.01) -> np.ndarray: ...
def leaky_relu_backward(grad_output, x, negative_slope=0.01) -> np.ndarray: ...
```

Mirrors `torch.nn.functional.leaky_relu`.

## Theory

Plain ReLU's biggest practical failure mode is the "dying ReLU" problem: once a unit's input goes negative on every training example, its output and gradient are both permanently `0`, `01-relu`'s backward returns exactly `0` for `x <= 0`, so that unit's weights never update again, it is dead for good.

LeakyReLU's fix is to replace ReLU's hard `0` for negative inputs with a small nonzero slope:

```text
LeakyReLU(x) = x              if x > 0
             = negative_slope * x   otherwise
```

with `negative_slope` typically a small constant like `0.01`. Negative inputs still shrink toward `0`, preserving ReLU's sparsity-inducing behavior, but they keep a small, nonzero gradient:

```text
d/dx LeakyReLU(x) = 1              if x > 0
                   = negative_slope otherwise
```

so a unit that goes negative can still receive a (small) gradient signal and recover, rather than dying permanently.

## Explanation

`leaky_relu_forward` uses `np.where(x > 0, x, negative_slope * x)`, the piecewise definition from Theory, applied elementwise.

`leaky_relu_backward` uses `np.where(x > 0, 1.0, negative_slope)` for the local derivative, then multiplies by `grad_output`, the same "compute the local slope, then chain-rule multiply" shape `01-relu`'s backward uses.
