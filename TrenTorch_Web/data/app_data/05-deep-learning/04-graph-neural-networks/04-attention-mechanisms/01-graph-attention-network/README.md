---
name: dl-graph-gat
title: Graph Attention Network
tags: [deep-learning, graph-neural-networks, gat]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Graph Attention Network (GAT) uses attention mechanisms to aggregate neighbor information. Each node computes attention weights for its neighbors, giving more weight to important neighbors.

$$h_i^{(l+1)} = \sigma\left(\sum_{j \in \mathcal{N}(i)} \alpha_{ij}^{(l)} W^{(l)} h_j^{(l)}\right)$$

Where alpha_ij are attention weights computed from node features.

### From theory to code

Implement:

```python
gat_attention_weights(features, adj)
```

Computes attention weights for each edge in the graph.

### Constraints

- features shape: (num_nodes, feature_dim).
- adj shape: (num_nodes, num_nodes), binary adjacency.
- Return shape: (num_nodes, num_nodes), attention weights.

## Theory

GAT learns which neighbors are important dynamically. Flexible and interpretable; attention weights explain the model.

## Explanation

Compute pairwise attention scores via dot product, mask non-edges, apply softmax per node.
