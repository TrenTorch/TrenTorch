---
name: dl-core-backward-multiplication
title: Backward for multiplication
tags: [neural-networks, autograd]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`Backward for addition` was almost suspiciously simple, the local derivative didn't even depend on the input VALUES, just the operation. Multiplication breaks that pattern immediately: `z = a * b`'s sensitivity to `a` depends directly on what `b` happens to be (double `b` and a nudge to `a` moves `z` twice as much), and vice versa. This is the first operation in this track whose backward rule genuinely needs to remember something about the FORWARD pass, the input values themselves, not just the operation's identity.

### From theory to code

Theory applies the chain rule to `z = a * b`: `dz/da = b` and `dz/db = a`, so the gradient flowing back to each input is the upstream gradient scaled by the OTHER input's value.

Implement `mul_backward(grad_output, a, b)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- Unlike `add_backward`, this function needs `a` and `b`'s actual values, not just `grad_output`.
- Return `(dL/da, dL/db)`, in that order.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`d(a*b)/da = b` (treating `b` as a constant while differentiating with respect to `a`), and symmetrically `d(a*b)/db = a`.

</details>

<details>
<summary>Hint 2</summary>

`grad_a = grad_output * b`, `grad_b = grad_output * a`, each input's gradient is scaled by the OTHER input, not its own.

</details>

## Theory

### The simple version

Total revenue is `price * quantity_sold`. If quantity sold is huge, a tiny bump in price adds up to a lot of extra revenue (price's sensitivity depends on quantity). If price is tiny, a tiny bump in quantity barely moves revenue at all (quantity's sensitivity depends on price). Each factor's importance to the product is scaled by how large the OTHER factor is, precisely the pattern multiplication's derivative captures.

### The formula

For `z = a * b`, the chain rule gives:

```text
dL/da = dL/dz * dz/da = grad_output * b
dL/db = dL/dz * dz/db = grad_output * a
```

Each input's gradient is the upstream gradient, scaled by the OTHER input's value, a genuinely different shape from addition's "just copy it through" rule. This is also the first hint at a pattern that recurs throughout this entire curriculum's backward passes: an operation's backward rule frequently needs to remember something from its OWN forward pass (here, both input values) to compute correctly, exactly why real autograd engines (built in `Graph node (value + grad + backward fn)`, later in this track) save forward-pass values specifically so backward has them available later.

### How PyTorch actually implements this

Every `*` between two `torch.Tensor`s with `requires_grad=True` registers a `MulBackward0` node holding onto both original tensors (or, in some fused cases, only whichever one backward actually still needs) specifically so this exact `grad_output * other_input` computation can run later, during `.backward()`, after the forward pass has already finished. This is also, structurally, identical to `03-tanh`'s own backward, `grad_output * (1 - output**2)`: an elementwise product involving the upstream gradient and some quantity from the forward pass, the same shape multiplication's backward rule establishes here in its purest, simplest form.

## Explanation

`mul_backward` returns `(grad_output * b, grad_output * a)`, each input's gradient scaled by the OTHER input's value, exactly the chain-rule formula from Theory.
