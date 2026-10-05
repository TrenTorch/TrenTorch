---
name: dl-graph-transe
title: TransE
tags: [deep-learning, graph-neural-networks, transe]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

TransE is a knowledge graph embedding model. For each triplet (h, r, t), it learns embeddings such that h + r ≈ t. The energy function penalizes violations of this relation.

$$E(h, r, t) = ||h + r - t||_2$$

### From theory to code

Implement:

```python
transe_score(h, r, t)
```

Computes TransE energy for triplet.

### Constraints

- h, r, t shape: (embedding_dim,).
- Return: scalar score (lower is better).

## Theory

TransE translates head by relation to reach tail. Simple, effective for knowledge graph completion.

## Explanation

Compute h + r - t. Take L2 norm. Return as score.
