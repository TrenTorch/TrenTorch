---
name: dl-graph-chebyshev
title: Chebyshev Graph Convolution
tags: [deep-learning, graph-neural-networks, chebyshev]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Chebyshev Graph Convolution uses Chebyshev polynomials of the graph Laplacian to define convolutional filters. This avoids eigendecomposition while being expressive.

$$g(\Lambda) \approx \sum_{k=0}^{K} \theta_k T_k(\tilde{\Lambda})$$

Where T_k is the k-th Chebyshev polynomial and tilde(Lambda) is normalized Laplacian eigenvalues.

### From theory to code

Implement:

```python
chebyshev_conv(features, adj, weight, k=3)
```

Applies k-order Chebyshev convolution.

### Constraints

- features shape: (num_nodes, input_dim).
- adj shape: (num_nodes, num_nodes).
- weight shape: (k+1, input_dim, output_dim).
- Return shape: (num_nodes, output_dim).

## Theory

Chebyshev convolution is computationally efficient and spectral-based. Enables efficient localized filtering.

## Explanation

Compute Laplacian. Normalize. Compute Chebyshev polynomials up to order k. Apply weighted sum.
