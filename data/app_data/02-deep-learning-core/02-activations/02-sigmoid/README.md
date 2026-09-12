---
name: dl-core-sigmoid
title: Sigmoid fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Beginner
---

## Statement

Implement:

```python
def sigmoid_forward(x) -> np.ndarray: ...
def sigmoid_backward(grad_output, output) -> np.ndarray: ...
```

- `sigmoid_backward` takes `output` (the forward pass's own saved result), not the original `x`, a genuinely different requirement from `01-relu`'s backward pass.

## Theory

`01-classical-ml/02-classification`'s `sigmoid` computed the same forward formula, `1 / (1 + exp(-x))`. This question adds the backward pass, and it has a real, useful property `01-relu`'s backward didn't: sigmoid's derivative can be written entirely in terms of its own _output_, `f'(x) = f(x) * (1 - f(x))`, with no reference to `x` at all.

```text
forward:  y = sigmoid(x)
backward: dL/dx = dL/dy * y * (1 - y)     -- needs y (the SAVED output), not x
```

This matters in practice: a real autograd engine (like the one `04-autograd`'s progressive build assembles later in this section) has to decide what to _save_ from the forward pass for the backward pass to use later. Saving `y` instead of `x` for a sigmoid, whenever both would work, is a real memory-efficiency choice, and for sigmoid specifically, `y` is strictly sufficient, there's never a reason to also keep `x` around.

## Explanation

`sigmoid_forward` clips `x` to `[-500, 500]` before exponentiating (the same guard `01-classical-ml`'s own `sigmoid` uses), `exp` of a very large negative number underflows harmlessly to `0`, but `exp` of a very large _positive_ number (from `-x` when `x` is very negative) can overflow to `inf`, clipping the input keeps the exponent itself bounded.

`sigmoid_backward` is the formula directly, `grad_output * output * (1 - output)`, the chain rule applied using only the saved forward output, exactly as Theory describes, no recomputation of `sigmoid_forward` and no need for the original `x` anywhere in this function.
