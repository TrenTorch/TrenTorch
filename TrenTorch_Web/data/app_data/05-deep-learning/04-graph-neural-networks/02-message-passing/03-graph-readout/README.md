---
name: dl-graph-readout
title: Graph Readout
tags: [deep-learning, graph-neural-networks, readout]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Graph Readout aggregates node-level representations into a single graph-level representation. Common readout functions include sum, mean, and max pooling.

$$h_G = \text{READOUT}(\{h_i^{(L)} : i \in V\})$$

Where READOUT is a permutation-invariant aggregation function.

### From theory to code

Implement:

```python
graph_readout(node_features, readout_type='sum')
```

Aggregates node features into a graph-level representation.

### Constraints

- node_features shape: (num_nodes, feature_dim).
- readout_type in ('sum', 'mean', 'max').
- Return shape: (feature_dim,).

## Theory

Graph readout enables graph-level classification/regression. Must be permutation-invariant.

## Explanation

Sum: add all node features. Mean: average. Max: element-wise maximum.
