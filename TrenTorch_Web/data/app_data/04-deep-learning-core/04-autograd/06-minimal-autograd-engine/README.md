---
name: dl-core-minimal-autograd-engine
title: Assemble minimal autograd engine
tags: [neural-networks, autograd]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Every piece is now built: `Graph node (value + grad + backward fn)` gave every `Value` a local `_backward` rule and the ability to record its own parents. `Topological sort for backward pass` gave a way to order every node in a graph so processing it in reverse guarantees each node's OWN gradient is fully accumulated before it needs to push gradient further backward. This question is the payoff: wire those two pieces together into `backward(root)`, a single function that computes gradients for an ENTIRE expression, of any depth, with any amount of variable reuse, with one call.

This is, in miniature, exactly what `loss.backward()` does in real PyTorch, `03-tanh`, `04-softmax`, every hand-derived gradient this curriculum has written up to this point was doing, by hand, precisely what this one function now does automatically, for any expression built from `+` and `*`.

### From theory to code

Theory seeds the output node's gradient at `1.0` (the starting point, "how much does the output change with respect to itself"), builds the topological order from that output, and calls every node's `_backward` in REVERSE topological order, guaranteeing each node's gradient is complete before it's used to push gradient further back.

Implement `backward(root)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- Seed `root.grad = 1.0` before calling any `_backward`.
- Process nodes in REVERSE topological order (root first, leaves last).
- After `backward(root)` runs, every reachable `Value`'s `.grad` must be correct, verified against a finite-difference check or real PyTorch, not just "it runs without error."

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`build_topo_order(root)` (already imported) gives you the forward-dependency order; Python's `reversed(...)` turns that into the backward-processing order directly.

</details>

<details>
<summary>Hint 2</summary>

The whole function is four lines: get the topo order, set `root.grad = 1.0`, loop over `reversed(topo_order)`, call `node._backward()` each time.

</details>

## Theory

### The simple version

A company's total profit depends on regional sales, which depend on store sales, which depend on individual transactions. To figure out "how much would total profit change if THIS ONE transaction changed," you'd need to trace the dependency chain all the way from the top (total profit) down to that one transaction, at each step asking "how does this level depend on the level below it," and multiplying those sensitivities together along the way. `backward` does exactly this, automatically, for a computation graph: start at the top (`root.grad = 1.0`, "how does the output depend on itself, trivially, completely"), then walk down through every dependency, in the right order, letting each node's own local rule push the right fraction of gradient down to whatever it depends on.

### The formula

```text
backward(root):
    topo_order = build_topo_order(root)   # forward-dependency order, root last
    root.grad = 1.0                        # d(root)/d(root) = 1
    for node in reversed(topo_order):      # root first, leaves last
        node._backward()                   # push gradient into this node's own parents
```

The REVERSE of the topological order is exactly right because of what `Topological sort for backward pass`'s own ordering guarantees: by the time any node `X` is reached in this reversed walk, every node that uses `X`'s output (every node that comes AFTER `X` in the forward order, meaning BEFORE `X` in the reversed order) has already had its `_backward` called, so `X.grad` is FULLY accumulated, every contribution from every place `X` was used has already arrived, before `X._backward()` runs and pushes gradient onward into `X`'s own parents. Processing nodes in any other order risks calling `_backward` on a node whose `.grad` is still incomplete, silently computing a wrong gradient for everything downstream of that mistake.

### How PyTorch actually implements this

`loss.backward()` on a real `torch.Tensor` performs exactly this algorithm, at scale: seed the loss tensor's gradient at `1.0` (or, for a non-scalar tensor, an explicitly-provided gradient), walk the recorded computation graph in the correct reverse-topological order, and call each node's own backward function (`AddBackward0`, `MulBackward0`, `MmBackward0`, the exact operations `Backward for addition`, `Backward for multiplication`, and `Backward for matmul` implemented individually earlier in this track), accumulating gradients into every leaf tensor's `.grad` along the way. Every gradient this curriculum has computed by hand so far, `03-mse-gradient`'s, `03-tanh`'s, is precisely what THIS function, generalized to arbitrary computation graphs and vectorized to tensors instead of scalars, computes automatically for any expression at all, this is, in miniature, the entire mechanism deep learning training is built on.

## Explanation

`backward` builds the topological order from `root` via the imported `build_topo_order`, sets `root.grad = 1.0`, and iterates `reversed(topo_order)`, calling each node's `_backward()` method in turn, exactly the algorithm from Theory. After this single loop finishes, every `Value` reachable from `root` holds its correct, fully-accumulated gradient.
