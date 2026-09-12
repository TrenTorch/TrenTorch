---
name: dl-core-relu
title: ReLU fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Beginner
---

## Statement

Implement:

```python
def relu_forward(x) -> np.ndarray: ...
def relu_backward(grad_output, x) -> np.ndarray: ...
```

- `relu_backward`'s gradient at exactly `x == 0` is `0` (PyTorch's own convention, one of several mathematically defensible choices at a non-differentiable point, but the one real PyTorch uses).

## Theory

This is the first of eight "forward and backward" activation function questions. Every one of them follows the same shape: `_forward` computes the activation itself, `_backward` computes how a gradient flowing backward through the network should be modified by having passed through this activation, `03-mse-gradient`'s chain-rule reasoning, applied to a nonlinearity instead of a linear layer.

**ReLU** (Rectified Linear Unit), `f(x) = max(0, x)`, is the simplest possible nonlinearity that's still useful: it passes positive values through unchanged and zeroes out negative ones. Its derivative is equally simple, `f'(x) = 1` where `x > 0` (the identity function's slope), `f'(x) = 0` where `x < 0` (a flat, zero-slope line), and technically undefined exactly at `x = 0` (a sharp corner), where real implementations just pick a convention, `0`, and move on.

```text
forward:  y = max(0, x)
backward: dL/dx = dL/dy * (1 if x > 0 else 0)
```

The backward pass needs the _original input_ `x` (not the forward output `y`), specifically to know which elements were positive, this is a genuinely different requirement from some of the later activation questions in this track, whose backward passes turn out to be cheaper to compute from their own _output_ instead.

## Explanation

`relu_forward` is `np.maximum(0.0, x)` directly, the elementwise max operation is the entire definition.

`relu_backward` builds a mask, `(x > 0).astype(grad_output.dtype)`, `1.0` wherever the original input was positive, `0.0` everywhere else (including exactly at `0`), and multiplies it into `grad_output` elementwise, this is the chain rule: the incoming gradient passes through unchanged wherever ReLU's slope was `1`, and gets zeroed out wherever ReLU's slope was `0`.
