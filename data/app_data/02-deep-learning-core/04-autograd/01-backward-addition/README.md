---
name: dl-core-backward-addition
title: Backward for addition
tags: [neural-networks, autograd]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`Chain rule: composing two functions' derivatives by hand` (Math & Statistics) established that every "backward" this curriculum has written, `03-tanh`'s, `04-softmax`'s, is the chain rule applied to one specific operation's own local derivative. Building a GENERAL autograd engine (this track's final goal) means giving every basic arithmetic operation its own tiny, self-contained backward rule, one per operation, that the engine can call automatically once it knows which operations were used to build an expression.

This question is the very first, simplest one: addition. `z = a + b`'s local derivative with respect to each input is about as simple as a derivative gets, and getting this one exactly right, and understanding WHY it's this simple, is the foundation every later, more complex backward rule in this track builds on.

### From theory to code

Theory applies the chain rule to `z = a + b`: since each input's LOCAL derivative is exactly `1`, the chain rule says the gradient flowing back to each input is just the upstream gradient, unchanged.

Implement `add_backward(grad_output)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `grad_output` is `dL/dz`, the gradient flowing IN from whatever used `z = a + b`'s result.
- Return `(dL/da, dL/db)`, in that order.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`d(a+b)/da = 1` and `d(a+b)/db = 1`, always, regardless of what `a` and `b` actually are.

</details>

<details>
<summary>Hint 2</summary>

The chain rule multiplies the local derivative by the upstream gradient: `1 * grad_output = grad_output`, for both `a` and `b`.

</details>

## Theory

### The simple version

If you're paid a dollar for every unit you produce, and you produce units two ways, a morning shift and an afternoon shift, adding those two shifts' output together to get your daily total, then one more unit from EITHER shift is worth exactly one more dollar. It doesn't matter which shift the extra unit came from, addition passes credit straight through, undiminished, to both of its inputs equally.

### The formula

For `z = a + b`, the chain rule (`Chain rule: composing two functions' derivatives by hand`) gives:

```text
dL/da = dL/dz * dz/da = grad_output * 1 = grad_output
dL/db = dL/dz * dz/db = grad_output * 1 = grad_output
```

Addition's defining property in a computation graph: it simply COPIES the incoming gradient to every one of its inputs, unchanged. This is the simplest possible backward rule in the entire autograd engine this track builds, every input to a sum receives the exact same gradient the sum itself received, no scaling, no transformation.

### How PyTorch actually implements this

Every `+` between two `torch.Tensor`s with `requires_grad=True` registers a `AddBackward0` node in the autograd graph at the moment the addition happens, and that node's backward rule is precisely this one, copy the incoming gradient to both operands (with an extra broadcasting-aware sum-reduction step if the two operands had different shapes, a detail this scalar version sidesteps). This exact behavior is also why `torch.nn.functional.linear`'s bias addition (`input @ weight.T + bias`) sends the SAME upstream gradient straight through to `bias`'s own gradient, unchanged, addition never modifies what flows through it, only copies it to every input.

## Explanation

`add_backward` returns `(grad_output, grad_output)` directly: addition's local derivative with respect to each input is exactly `1`, so the chain rule leaves the upstream gradient completely unchanged for both.
