---
name: dl-graph-link-prediction
title: Link Prediction
tags: [deep-learning, graph-neural-networks, link-prediction]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Link prediction predicts missing or future edges in a graph. Given node embeddings h_u and h_v, score the likelihood of an edge. Common scorers: dot product, Euclidean distance, or MLP.

$$s(u, v) = h_u^T h_v$$

### From theory to code

Implement:

```python
link_prediction_score(u_emb, v_emb, method='dot')
```

Scores edge likelihood between two nodes.

### Constraints

- u_emb, v_emb shape: (embedding_dim,).
- method in ('dot', 'euclidean', 'cosine').
- Return: scalar score.

## Theory

Link prediction enables knowledge graph completion, missing link recovery, and future link prediction.

## Explanation

Dot: inner product. Euclidean: negative L2 distance. Cosine: normalized dot product.
