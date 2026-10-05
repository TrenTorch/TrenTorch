---
name: dl-graph-gin
title: Graph Isomorphism Network
tags: [deep-learning, graph-neural-networks, gin]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Graph Isomorphism Network (GIN) uses the Weisfeiler-Lehman test to aggregate node information. It has provably high expressive power for distinguishing non-isomorphic graphs.

$$h_i^{(l+1)} = \text{MLP}^{(l)}\left((1 + \epsilon^{(l)}) h_i^{(l)} + \sum_{j \in \mathcal{N}(i)} h_j^{(l)}\right)$$

Where epsilon is a learnable parameter (can be fixed).

### From theory to code

Implement:

```python
gin_layer(features, adj, weight, epsilon=0.0)
```

### Constraints

- features shape: (num_nodes, input_dim).
- adj shape: (num_nodes, num_nodes).
- weight shape: (input_dim, output_dim).
- epsilon: scalar, learnable or fixed.
- Return shape: (num_nodes, output_dim).

## Theory

GIN provably distinguishes all non-isomorphic graphs in standard settings. Highly expressive for graph-level tasks.

## Explanation

Aggregate neighbor features. Scale center node by (1+epsilon). Concatenate. Apply MLP (linear transformation).
