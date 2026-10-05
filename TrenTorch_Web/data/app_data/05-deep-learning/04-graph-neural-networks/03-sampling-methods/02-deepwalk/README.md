---
name: dl-graph-deepwalk
title: DeepWalk
tags: [deep-learning, graph-neural-networks, deepwalk]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

DeepWalk learns node embeddings by performing random walks on the graph and treating walks as sentences. Node embeddings are learned via Skip-gram, learning to predict context nodes from center nodes.

### From theory to code

Implement:

```python
random_walk(adj, start_node, walk_length)
```

Performs a random walk on the graph starting from a node.

### Constraints

- adj shape: (num_nodes, num_nodes).
- start_node: index of starting node.
- walk_length: length of walk sequence.
- Return shape: (walk_length,), node indices in walk.

## Theory

DeepWalk preserves network structure in embedding space. Nodes with similar local neighborhoods have similar embeddings.

## Explanation

At each step, randomly select a neighbor of current node. Continue for walk_length steps.
