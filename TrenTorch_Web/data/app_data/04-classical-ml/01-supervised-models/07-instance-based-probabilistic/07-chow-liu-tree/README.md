---
name: bayes-chow-liu-tree
title: 'Chow-Liu tree from mutual information'
tags: [classical-ml, bayesian-networks, mutual-information, spanning-tree]
difficulty: Advanced
---

## Statement

### Learn the strongest tree of pairwise dependencies

A tree-structured Bayesian network is a cheap model of a joint distribution over discrete variables. The Chow-Liu algorithm picks the tree that maximizes the total pairwise mutual information between connected variables. It is a maximum spanning tree problem where each edge weight is a mutual information.

Implement two functions.

- `mutual_information(a, b)`: the mutual information in bits between two 1-D discrete arrays of the same length. Use the empirical joint distribution.
- `chow_liu_tree(X)`: `X` is an `n` by `d` array of discrete columns. Return a sorted list of `(i, j)` tuples with `i < j` for the edges of a maximum spanning tree over the `d` columns.

### Constraints

- `mutual_information` raises `ValueError` if the inputs are not 1-D with the same length.
- `chow_liu_tree` raises `ValueError` if `X` is not 2-D. It returns `[]` when `d = 1`.
- Return exactly `d - 1` edges for `d >= 1`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Kruskal's algorithm works directly: sort the pairs by mutual information in descending order, then add each edge that joins two different components. A small union-find handles the components.

</details>

## Theory

Mutual information `I(A; B)` is zero when the two variables are independent and equals the entropy of one of them when one determines the other. Chow and Liu showed that among all tree-structured models, the one with the highest likelihood is the maximum spanning tree under these weights. The result gives an approximation with exactly `d - 1` parameters per conditional table, which is much smaller than a full joint table.

### Where this shows up in production

Tree-augmented and tree-structured Bayesian networks show up in fraud and reliability analysis, where a few discrete event flags need a joint model that scores unusual combinations. Chow-Liu trees are also a fast structure learner for causal discovery pipelines that later refine the result with domain knowledge. A common production use is as a density model that flags rows with low probability under the tree.

### Using it to make decisions

Use it when you need a joint model over many discrete variables and cannot afford a full table or a search over all DAGs. Check the mutual information values before you trust the tree: if all edges have values near zero, the tree is arbitrary and the model is no better than independence. Mutual information on small samples is biased upward, so use a minimum sample count or a correction before you keep weak edges.

### Pros and cons

**Pros:** the algorithm is polynomial, the result is the best tree in likelihood, and the parameters are cheap to estimate and to store.

**Cons:** a tree can only express one parent per variable, so real dependencies with two strong causes are lost. Mutual information ignores the direction of the dependency, so the tree does not give causal arrows. The estimate is biased on small data, and the edges are unstable when two dependencies are nearly equal.

## Explanation

The solution computes the empirical joint table for each pair of columns and evaluates the mutual information from it. It then runs Kruskal's algorithm on the pairs in descending order, using a union-find structure to skip edges that would form a cycle.
