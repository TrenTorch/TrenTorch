---
name: cosine-knn-vote-company-207
title: 'cosine-knn-vote — Spotify case'
tags: [problemset, classical-ml, knn, spotify]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Spotify'
hint: 'cosine similarity to every row, argmax, return that row’s label'
tools: [NumPy]
---

## Statement

Spotify-inspired recommendation prototype uses nearby embedding vectors to infer a label from similar items. You need to find the training item most similar to the query by cosine similarity and return its class so the team can validate the retrieval baseline.

Find the training vector most similar to the query by cosine similarity and return its class. If several vectors tie, the first one wins; a vector with zero length has similarity $0$ to everything.

Implement `solve(X, y, q)`.

**Returns.** Return the label (an element of `y`) of the most similar training row.

Find the training vector most similar to the query by cosine similarity and return its class. If several vectors tie, the first one wins; a vector with zero length has similarity $0$ to everything.

Implement `solve(X, y, q)`.

**Returns.** Return the label (an element of `y`) of the most similar training row.

### Examples

**Example 1**

Input:

```python
solve([[1, 0], [0, 1]], ['A', 'B'], [0.9, 0.1])
```

Output:

```text
'A'
```

**Example 2**

Input:

```python
solve([[1, 0], [1, 1], [0, 1]], ['x', 'y', 'z'], [0.1, 1.0])
```

Output:

```text
'z'
```

## Theory

### The simple version

Embedding models place similar items close together in direction. Cosine similarity measures the angle between two vectors and ignores their lengths, so it is the usual way to compare embeddings. The 1-nearest-neighbour rule then copies the class of the single most similar training item.

### The formula

$$\cos(x,q)=\frac{x\cdot q}{\|x\|\,\|q\|},\qquad \hat y=y_{\arg\max_i\cos(x_i,q)}$$

### Why it matters

- Embeddings of similar items point in similar directions, so cosine similarity is the usual way to compare them.
- The 1-nearest-neighbour rule copies the class of the most similar training item.

### How it works

1. Compute the cosine similarity of the query with every training row (zero if a norm is zero).
2. Take the row with the highest similarity.
3. Return its label.

### Worked example

The query $(0.9,0.1)$ has cosine $0.9/\sqrt{0.82}=0.994$ with $(1,0)$ and $0.1/\sqrt{0.82}=0.110$ with $(0,1)$, so the first row wins and the label is 'A'.

## Explanation

All similarities are computed at once as a matrix-vector product divided by the product of the norms. The zero-norm guard sets those scores to $0$ instead of dividing by zero. In the second example the query $(0.1,1)$ points almost exactly along $(0,1)$, so class `'z'` wins.
