---
name: dl-training-sgd
title: SGD
tags: [optimization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`04-gd-step` (Classical ML) already implemented gradient descent's update rule, but specifically for one weight matrix and one bias vector, `linear_regression`'s own two parameters. A real neural network has dozens, sometimes billions, of parameters spread across many layers, and every single one of them needs the exact same update rule applied, independently, every training step. This question generalizes `04-gd-step`'s specific update into the general form every optimizer in this track (and every optimizer in `torch.optim`) actually takes: operate on a LIST of parameters and their gradients, applying one uniform rule to all of them at once.

### From theory to code

Theory applies the identical "step opposite the gradient" rule from `04-gd-step` to every `(parameter, gradient)` pair in two lists, independently.

Implement `sgd_step(params, grads, lr)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `params` and `grads` are parallel lists (same length, matched by index).
- Return a NEW list, don't mutate the input arrays in place.
- Every parameter uses the SAME learning rate `lr`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

This is `04-gd-step`'s exact update formula, `param - lr * grad`, applied inside a loop (or list comprehension) over every parameter.

</details>

<details>
<summary>Hint 2</summary>

`[p - lr * g for p, g in zip(params, grads)]` is the entire function, in one line.

</details>

## Theory

### The simple version

`04-gd-step` already explained the core idea, step opposite the gradient, scaled by a learning rate, for one weight and one bias. A real network doesn't have just one weight and one bias, it has an entire COLLECTION of parameters, spread across every layer, and training means applying that exact same nudge to every single one of them, every step, based on ITS OWN gradient (how much THAT specific parameter, and only that parameter, would help reduce the loss if nudged).

### The formula

```text
sgd_step(params, grads, lr)[i] = params[i] - lr * grads[i]
```

applied independently to every `(parameter, gradient)` pair. This is exactly `04-gd-step`'s formula, `weight - lr * grad_weight`, generalized from "exactly one weight array" to "however many parameter arrays a model happens to have," the shape every real optimizer actually operates in: PyTorch's own `torch.optim.Optimizer` base class stores a flat list of parameters (or groups of them) internally and applies each optimizer's own update rule to every one of them, uniformly, every `.step()` call.

### How PyTorch actually implements this

`torch.optim.SGD` implements exactly this update rule (plus optional momentum, weight decay, and Nesterov acceleration, all off by default, `SGD + Momentum`, the next question in this track, builds the momentum extension directly). Calling `optimizer.step()` in a real training loop internally does precisely what `sgd_step` does here: iterate over every registered parameter, read its `.grad` (populated by the preceding `loss.backward()` call, `Assemble minimal autograd engine`'s own mechanism, generalized to tensors), and update it in place using the optimizer's rule. `optimizer.zero_grad()`, called at the start of every training loop iteration, exists specifically to reset each parameter's accumulated gradient to zero before the NEXT `backward()` call, without it, gradients from consecutive batches would silently accumulate on top of each other, exactly the accumulation behavior `Graph node (value + grad + backward fn)` built deliberately, but which needs an explicit reset between independent training steps.

## Explanation

`sgd_step` returns a new list, one entry per `(param, grad)` pair, each computed as `param - lr * grad`, exactly `04-gd-step`'s own update formula applied uniformly across every parameter in the list.
