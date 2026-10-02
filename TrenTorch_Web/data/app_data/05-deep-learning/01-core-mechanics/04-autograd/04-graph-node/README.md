---
name: dl-core-graph-node
title: Graph node (value + grad + backward fn)
tags: [neural-networks, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Backward for addition`, `Backward for multiplication` and `Backward for matmul` each computed a LOCAL backward rule, given some upstream gradient, produce the gradient for each input, as a one-off function call. A real autograd engine needs more: it needs to remember, automatically, WHICH operations built which values, in what order, so that calling `.backward()` once, at the very end of a computation, can walk backward through every operation that happened and apply each one's local rule in the right order, without a human manually chaining the calls together.

This question builds the object that makes that possible: a graph NODE that doesn't just hold a number, it also remembers its own parents (what it was built from) and carries its own `_backward` function (how to push gradient into those parents), attached automatically the moment an operation creates it.

### From theory to code

Theory wraps `Backward for addition` and `Backward for multiplication`'s formulas into `Value`'s `__add__` and `__mul__` operator overloads: each one builds a new `Value` recording its own parents, and attaches a `_backward` closure that, when called, applies that operation's backward formula and ACCUMULATES (not overwrites) gradient into each parent.

Implement `Value.__add__` and `Value.__mul__` against that reasoning. The class skeleton, `__init__`, and docstrings are already in the editor.

### Constraints

- `other` may be a plain Python number, not just a `Value`, wrap it in `Value(other)` first.
- Gradient must ACCUMULATE (`+=`), never overwrite (`=`), a node used in more than one place needs contributions from every place it was used, added together.
- `out._backward` must be attached as a closure capturing `self`, `other`, and `out` (via Python's closure scoping, not passed as explicit arguments).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`Backward for addition`'s rule was `(grad_output, grad_output)`; inside `_backward`, `grad_output` is simply `out.grad` (the parent's own accumulated gradient, set by whatever comes later).

</details>

<details>
<summary>Hint 2</summary>

Define `_backward` as a nested function INSIDE `__add__`/`__mul__` (so it closes over `self`, `other`, `out` automatically), then assign it: `out._backward = _backward`.

</details>

## Theory

### The simple version

A spreadsheet cell computed as `=B2+C2` doesn't just show a number, it also remembers the FORMULA that produced it, which is exactly what lets a spreadsheet propagate changes: edit `B2`, and every cell whose formula depends on it updates automatically, because each cell remembers what it was built from. `Value` does the analogous thing for gradients instead of values: every node remembers what operation built it and which nodes it came from, specifically so gradient can later be pushed backward through that same chain, automatically, without recomputing anything by hand.

### The formula

Each `Value` carries:

```text
data       -- the actual scalar value (the "forward pass" result)
grad       -- accumulated gradient (starts at 0, filled in during backward)
_prev      -- the set of Value nodes this one was built from
_backward  -- a closure: "given MY OWN .grad, push gradient into _prev"
```

`__add__` and `__mul__` each build a new `Value` and immediately attach the RIGHT `_backward` closure for that specific operation, `Backward for addition`'s and `Backward for multiplication`'s formulas respectively, using `out.grad` in place of the `grad_output` parameter those earlier questions took explicitly. The closure captures `self`, `other`, and `out` by Python's normal scoping rules (a nested function has access to its enclosing function's local variables), no need to pass them in explicitly.

Accumulation (`+=`) is the detail easiest to get wrong and most important to get right: if the SAME `Value` is used in two different places in an expression (`y = a + a`, or more realistically, a weight reused across multiple layers), each USE contributes its own gradient, and the correct total gradient is the SUM of every contribution, not just whichever one happened to run last. `Backward for addition` and `Backward for multiplication`'s own formulas already return the correct PER-USE contribution; `Value`'s job is making sure those contributions correctly ADD UP when a node has more than one.

### How PyTorch actually implements this

Every `torch.Tensor` with `requires_grad=True` carries a `grad_fn` attribute pointing to exactly this kind of node (a `AddBackward0`, `MulBackward0`, etc.), each one holding references to the tensors it needs for its own backward computation and knowing how to push gradient into its own inputs, precisely the `_prev`/`_backward` structure this question builds by hand, at real PyTorch's actual internal architecture's level of abstraction, just implemented in optimized C++ rather than plain Python. `.grad` accumulating via `+=` (rather than overwriting) is also real PyTorch's actual behavior, exactly why `optimizer.zero_grad()` exists as an explicit step at the start of every training loop, to reset accumulated gradients to zero before the next backward pass, otherwise gradients from consecutive batches would silently accumulate on top of each other.

## Explanation

`__add__` wraps `other` in a `Value` if needed, builds `out = Value(self.data + other.data, (self, other))`, and defines `_backward` as a closure that adds `out.grad` into both `self.grad` and `other.grad`, `Backward for addition`'s formula with `out.grad` standing in for `grad_output`.

`__mul__` follows the identical structure, with `_backward` implementing `Backward for multiplication`'s formula instead: `self.grad += other.data * out.grad`, `other.grad += self.data * out.grad`.
