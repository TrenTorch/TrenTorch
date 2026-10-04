---
name: dl-graph-weisfeiler-lehman
title: Weisfeiler-Lehman Test
tags: [deep-learning, graph-neural-networks, weisfeiler-lehman]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The Weisfeiler-Lehman (WL) test is a graph isomorphism heuristic. It iteratively refines node labels based on neighbor labels. Two graphs are deemed non-isomorphic if their label distributions differ at any iteration.

### From theory to code

Implement:

```python
weisfeiler_lehman(adj, num_iterations=3)
```

Performs WL iterations and returns final node color distributions.

### Constraints

- adj shape: (num_nodes, num_nodes), binary.
- num_iterations: number of WL refinement steps.
- Return shape: (num_nodes,), integer color labels.

## Theory

WL test determines the expressive power of GNNs. GNNs are at most as expressive as the 1-WL test.

## Explanation

Iterate: hash each node's label and neighbor labels. Update node label to hash. Return final labels.
