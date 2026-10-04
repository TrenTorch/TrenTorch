---
name: dl-graph-node2vec
title: node2vec
tags: [deep-learning, graph-neural-networks, node2vec]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

node2vec extends DeepWalk with biased random walks controlled by return parameter p and in-out parameter q. These parameters control exploration depth vs. breadth.

High p: discourage immediate returns to previous node. High q: breadth-first exploration.

### From theory to code

Implement:

```python
biased_random_walk(adj, start_node, walk_length, p, q)
```

### Constraints

- adj shape: (num_nodes, num_nodes).
- start_node, walk_length: int.
- p, q: positive floats (transition probabilities).
- Return shape: (walk_length,).

## Theory

node2vec balances local and global network structure. Different p, q values capture different node roles.

## Explanation

Use 2nd-order Markov chain: transition probs depend on previous node. Weight edges by p, q based on distance to previous.
