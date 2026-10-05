---
name: dl-graph-graphsage
title: GraphSAGE
tags: [deep-learning, graph-neural-networks, graphsage]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

GraphSAGE (Graph SAmple and aggreGatE) samples a neighborhood for each node and aggregates their features. Unlike GCN which uses all neighbors, GraphSAGE samples K neighbors for scalability.

$$h_i^{(l+1)} = \sigma(W^{(l)} \text{AGG}(\{h_j^{(l)} : j \in \mathcal{S}_i\}))$$

Where S_i is a sampled neighborhood of node i.

### From theory to code

Implement:

```python
graphsage_layer(features, adj, weight, num_samples)
```

Samples neighbors, aggregates, applies weight, returns updated features.

### Constraints

- features shape: (num_nodes, input_dim).
- adj shape: (num_nodes, num_nodes).
- weight shape: (input_dim, output_dim).
- num_samples: number of neighbors to sample.
- Return shape: (num_nodes, output_dim).

## Theory

GraphSAGE enables mini-batch training on large graphs via neighbor sampling. Practical for billion-scale graphs.

## Explanation

Sample up to K neighbors per node. Aggregate sampled neighbor features via mean. Apply weight matrix.
