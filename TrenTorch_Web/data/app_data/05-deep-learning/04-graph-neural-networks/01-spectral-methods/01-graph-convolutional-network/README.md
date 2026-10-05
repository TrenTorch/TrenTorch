---
name: dl-graph-gcn
title: Graph Convolutional Network
tags: [deep-learning, graph-neural-networks, gcn]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A Graph Convolutional Network (GCN) applies convolution-like operations on graphs. It aggregates neighbor information via message passing: each node updates its representation by aggregating its neighbors' representations.

$$h_i^{(l+1)} = \sigma\left(W^{(l)} \sum_{j \in \mathcal{N}(i)} \frac{1}{\sqrt{d_i d_j}} h_j^{(l)}\right)$$

Where N(i) is the neighborhood of node i, d_i is the degree, W is a learnable weight matrix, and sigma is an activation.

### From theory to code

Implement:

```python
gcn_layer(features, adj, weight)
```

Applies one GCN layer: aggregate neighbors, apply weight matrix, return node embeddings.

### Constraints

- features shape: (num_nodes, input_dim).
- adj shape: (num_nodes, num_nodes), adjacency matrix.
- weight shape: (input_dim, output_dim).
- Return shape: (num_nodes, output_dim).

## Theory

GCN learns node representations by iteratively aggregating neighborhood information. Works well for node classification and graph-level tasks.

## Explanation

Normalize adjacency matrix by degree. Multiply features by transpose of weight. Pre-multiply by normalized adjacency. Apply activation.
