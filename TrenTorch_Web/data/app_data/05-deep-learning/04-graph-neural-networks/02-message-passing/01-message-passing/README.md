---
name: dl-graph-message-passing
title: Message Passing Framework
tags: [deep-learning, graph-neural-networks, message-passing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Message Passing is a general framework for GNNs. Each node sends "messages" to neighbors. Neighbors aggregate these messages. Each node updates its representation using the aggregate.

$$m_i^{(l+1)} = \sum_{j \in \mathcal{N}(i)} f(h_i^{(l)}, h_j^{(l)})$$
$$h_i^{(l+1)} = g(h_i^{(l)}, m_i^{(l+1)})$$

Where f is a message function and g is an update function.

### From theory to code

Implement:

```python
message_passing(features, adj, message_fn)
```

### Constraints

- features shape: (num_nodes, feature_dim).
- adj shape: (num_nodes, num_nodes).
- message_fn: callable that takes (sender_features, receiver_features).
- Return shape: (num_nodes, feature_dim).

## Theory

Message Passing unifies all GNN variants (GCN, GAT, GraphSAGE, etc.) under one framework.

## Explanation

For each edge, compute message from sender to receiver. Aggregate messages per node. Return updated features.
