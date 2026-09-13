---
name: dl-core-tanh
title: Tanh fwd/bwd
tags: [deep-learning, activations, autograd]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`02-sigmoid` squashes its input into `(0, 1)` — always positive, which turns out to be a real practical downside for a hidden-layer activation: every unit downstream receives an always-positive signal, which tends to bias how gradients flow during training. Tanh is sigmoid's zero-centered cousin: the same S-shape, but squashed into `(-1, 1)` instead, so its output can be negative, positive, or exactly zero.

### From theory to code

`tanh(x) = 2*sigmoid(2x) - 1`, so it's the same family of function as `02-sigmoid`, and its derivative has the same "expressible purely in terms of the output" property. Implement `tanh_forward(x)` and `tanh_backward(grad_output, output)`, taking `output` (the saved forward result), not `x`, same pattern as `02-sigmoid`.

### Constraints

- `x`: any NumPy array shape. `tanh_forward` returns the same shape, values in `[-1, 1]`.
- `tanh_backward(grad_output, output)` takes the forward pass's own saved result, not the original `x`.
- `tanh_forward` must stay finite for any input, including very large `|x|`.
- No Python loops; no mutating the inputs.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

NumPy already has this forward function built in — no need to derive it from `exp` by hand.

</details>

<details>
<summary>Hint 2</summary>

Tanh's derivative, like sigmoid's, is written purely in terms of its own output: `f'(x) = 1 - f(x)^2`.

</details>

## Theory

### The simple version

Tanh is sigmoid with its output re-centered and re-scaled: same S-shape, same saturating behavior at the extremes, but shifted so "no signal" reads as `0` instead of `0.5`, and stretched so the full range spans `-1` to `1` instead of `0` to `1`. A downstream layer receiving tanh's output sees genuinely negative and positive values, rather than sigmoid's everything-is-positive signal — which in practice tends to make training somewhat better-behaved.

### The formula

```text
forward:  y = tanh(x)
backward: dL/dx = dL/dy * (1 - y^2)
```

Being zero-centered (its output ranges symmetrically around `0`, unlike sigmoid's `(0,1)` range which is always positive) is tanh's practical advantage over sigmoid as a hidden-layer activation — downstream layers receiving a zero-centered signal tend to train somewhat better than ones receiving an always-positive one. Both still share sigmoid's real weakness: `1 - y^2` shrinks toward `0` as `y` approaches either `-1` or `1`, the same vanishing-gradient shape `02-sigmoid`'s Theory names.

### How PyTorch actually implements this

Context only, untested by your submission: `torch.tanh` (and `nn.Tanh`) compute the same forward function, and PyTorch's autograd saves the forward output (not the input) to compute this backward pass, exactly the `1 - y^2` factor this exercise implements by hand.

## Explanation

`tanh_forward` is `np.tanh(x)` directly, NumPy's own implementation.

`tanh_backward` is `grad_output * (1 - output**2)`, the chain rule applied using only the saved forward output, exactly as Theory's formula states — no recomputation of `tanh_forward` and no need for the original `x`.
