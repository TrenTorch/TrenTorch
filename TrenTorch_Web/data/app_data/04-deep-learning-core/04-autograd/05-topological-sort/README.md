---
name: dl-core-topological-sort
title: Topological sort for backward pass
tags: [neural-networks, autograd]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`Graph node (value + grad + backward fn)` gave every `Value` its own `_backward` closure, capable of pushing gradient into its immediate parents, given its OWN gradient is already known. But for anything beyond a single operation, that raises an ordering question: in an expression like `c = a*b + a`, the intermediate node `a*b` needs ITS gradient computed before it can push gradient further back into `a` and `b`, and `c` needs to run first of all (it's the very output the whole backward pass starts from). Call `_backward` in the wrong order, on a node whose OWN `.grad` hasn't been fully accumulated yet, and you get a silently wrong answer, not a crash, just numbers that look plausible but aren't the real gradient.

Topological sort is the tool that guarantees the right order: an ordering of every node in the graph where every node appears strictly after everything it depends on, which, read in REVERSE, is exactly the order a correct backward pass needs to call every node's `_backward`.

### From theory to code

Theory performs a post-order depth-first traversal from the output node: recurse into every parent FIRST, then append the current node, after every parent has already been appended. This guarantees every node appears after all its ancestors in the returned list, with the starting node last.

Implement `build_topo_order(root)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- Track visited nodes so a node reachable through more than one path (the same aliasing scenario `Graph node`'s own accumulation tests exercise) appears exactly once in the result.
- `root` must be the LAST element of the returned list.
- Every parent of a node must appear BEFORE that node in the returned list.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Write a recursive helper: if a node hasn't been visited yet, mark it visited, recurse into every one of its `_prev` parents, THEN append the node itself, in that order.

</details>

<details>
<summary>Hint 2</summary>

Call the helper once, starting from `root`, and return whatever list it built up via its appends.

</details>

## Theory

### The simple version

Getting dressed has a strict order: socks before shoes, shirt before jacket. You couldn't correctly plan "which order do I put clothes on" by picking randomly, you need an order where each item comes after everything it depends on. A computation graph has the same structure: `a*b`'s result depends on `a` and `b` already existing, `c = (a*b) + a` depends on `a*b` already being computed. Topological sort finds exactly this valid dependency order, generalized to arbitrary graphs, not just getting-dressed.

### The formula

Post-order depth-first traversal from the output node:

```text
visit(node):
    if node not already visited:
        mark node visited
        for each parent in node._prev:
            visit(parent)          # recurse FIRST
        append node to the result  # THEN append, after all parents are in
```

Calling `visit(root)` once produces a list where `root` is LAST (everything else got appended before it finished recursing) and every node appears strictly after every one of its own ancestors. This is precisely the FORWARD computation order, the order values would need to be computed in, if you were computing the graph from scratch.

The backward pass needs the OPPOSITE direction: start from the output (whose gradient is `1`, or otherwise already known) and walk backward, only ever processing a node once every one of ITS OWN children has already contributed to its gradient. `Assemble minimal autograd engine`, the very next question in this track, reveals the answer directly: **reversing** this topological order gives exactly that, root first, then everything in an order where, by the time any node's `_backward` runs, every node that could still push MORE gradient into it has already done so.

### How PyTorch actually implements this

Real PyTorch's autograd engine performs conceptually the same topological traversal (implemented with an explicit priority queue over each node's `grad_fn`s rather than a simple recursive DFS, for both performance and to correctly handle wildly unbalanced graphs without risking Python's recursion limit), walking the graph backward from the final loss tensor exactly once per `.backward()` call. This is also precisely why calling `.backward()` twice on the SAME graph without `retain_graph=True` raises an error, PyTorch discards the graph structure (the `_prev`-equivalent bookkeeping) after one backward pass by default, specifically because keeping it around costs memory that's usually no longer needed once gradients have been computed.

## Explanation

`build_topo_order` defines a recursive `visit` helper that, for any not-yet-visited node, marks it visited, recurses into every one of its `_prev` parents FIRST, and only then appends the node itself to `topo_order`, guaranteeing every parent lands before its children in the final list. Calling `visit(root)` once and returning `topo_order` gives the complete, correctly-ordered traversal from Theory.
