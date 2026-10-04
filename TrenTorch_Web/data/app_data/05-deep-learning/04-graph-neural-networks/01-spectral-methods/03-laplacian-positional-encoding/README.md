---
name: dl-graph-laplacian-pe
title: Laplacian Positional Encoding
tags: [deep-learning, graph-neural-networks, positional-encoding]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Laplacian Positional Encoding (LPE) uses eigenvectors of the graph Laplacian as node features. The k smallest eigenvalues/eigenvectors capture global graph structure, useful for node classification and graph tasks.

$$\text{PE}_i = [\text{eigenvector}_1(i), \text{eigenvector}_2(i), ..., \text{eigenvector}_k(i)]$$

### From theory to code

Implement:

```python
laplacian_positional_encoding(adj, k=10)
```

Computes Laplacian PE for all nodes.

### Constraints

- adj shape: (num_nodes, num_nodes).
- k: number of eigenvectors to keep.
- Return shape: (num_nodes, k).

## Theory

LPE provides global structural information to GNNs. Nodes in similar graph positions have similar PEs.

## Explanation

Compute graph Laplacian. Eigendecompose. Return first k eigenvectors as node features.
