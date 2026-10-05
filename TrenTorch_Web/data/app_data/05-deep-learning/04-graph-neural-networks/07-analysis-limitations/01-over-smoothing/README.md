---
name: dl-graph-over-smoothing
title: Over-smoothing in GNNs
tags: [deep-learning, graph-neural-networks, over-smoothing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Over-smoothing is a phenomenon where node representations become indistinguishable after many GNN layers. Nodes converge to the same representation regardless of their local structure.

### From theory to code

Implement:

```python
detect_over_smoothing(features, adj, num_layers)
```

Measures over-smoothing by computing feature divergence after each layer.

### Constraints

- features shape: (num_nodes, feature_dim).
- adj shape: (num_nodes, num_nodes).
- num_layers: number of GNN layers to simulate.
- Return: divergence scores per layer.

## Theory

Over-smoothing limits GNN depth. Solutions: skip connections, regularization, heterogeneity-aware designs.

## Explanation

Apply averaging aggregation num_layers times. After each layer, measure feature divergence (variance across nodes). Lower variance indicates over-smoothing.
