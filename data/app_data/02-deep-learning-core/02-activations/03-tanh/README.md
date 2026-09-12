---
name: dl-core-tanh
title: Tanh fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Beginner
---

## Statement

Implement:

```python
def tanh_forward(x) -> np.ndarray: ...
def tanh_backward(grad_output, output) -> np.ndarray: ...
```

- `tanh_backward` takes `output` (the saved forward result), not `x`, same pattern as `02-sigmoid`.

## Theory

`tanh` is closely related to sigmoid, `tanh(x) = 2*sigmoid(2x) - 1`, both are S-shaped ("sigmoidal") curves that squash their input into a bounded range, sigmoid into `(0, 1)`, tanh into `(-1, 1)`. Tanh's derivative has the same "expressible purely in terms of the output" property sigmoid's does:

```text
forward:  y = tanh(x)
backward: dL/dx = dL/dy * (1 - y^2)
```

Being zero-centered (its output ranges symmetrically around `0`, unlike sigmoid's `(0,1)` range which is always positive) is tanh's practical advantage over sigmoid as a hidden-layer activation, downstream layers receiving a zero-centered signal tend to train somewhat better than ones receiving an always-positive one. Both still share sigmoid's real weakness: `1 - y^2` shrinks toward `0` as `y` approaches either `-1` or `1`, the same vanishing-gradient shape `02-sigmoid`'s Theory names.

## Explanation

`tanh_forward` is `np.tanh(x)` directly, NumPy's own implementation.

`tanh_backward` is `grad_output * (1 - output**2)`, the chain rule applied using only the saved forward output, exactly as Theory's formula states, no recomputation of `tanh_forward` and no need for the original `x`.
