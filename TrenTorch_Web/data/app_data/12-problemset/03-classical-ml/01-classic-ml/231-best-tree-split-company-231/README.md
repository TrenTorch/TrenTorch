---
name: best-tree-split-company-231
title: 'best-tree-split — Zoom case'
tags: [problemset, classical-ml-trees-ensembles, decision-trees, zoom]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'Classic ML'
caseCompany: 'Zoom'
hint: 'sort; for each change of value take the midpoint; keep the lowest weighted Gini'
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Zoom** ranking and experimentation team might handle; it is not a real interview question or a claim that Zoom uses this exact task. The team needs a reliable implementation for tree split in a production-oriented ML workflow. A subtle implementation error can pass obvious examples while producing incorrect behavior on boundary or distribution-shifted cases.

Evaluate candidate thresholds between sorted feature values and return the threshold with the lowest weighted Gini impurity.

Evaluate every candidate threshold and return the best one. Candidates are the midpoints between consecutive **distinct** sorted feature values; the score of a threshold is the sample-weighted Gini impurity of the two sides (labels are 0/1), and a later candidate must beat the best by more than $10^{-12}$, so ties keep the smaller threshold.

Implement `solve(x,y)`.

**Returns.** Return the threshold as a float, or `None` if `x` has fewer than two distinct values.

### Examples

**Example 1**

Input:

```python
solve([1, 2, 4, 7], [0, 0, 1, 1])
```

Output:

```text
3.0
```

**Example 2**

Input:

```python
solve([3.0, 3.0], [0, 1])
```

Output:

```text
None
```

## Theory

### The simple version

A decision tree chooses a question such as "is the value below $t$?" for each node. Among all possible thresholds, the best one yields two groups that are as pure as possible. Only midpoints between neighbouring _different_ values matter, since any cut between the same two neighbours gives the same split.

### The score

$$\text{score}(t)=\frac{n_L}{n}\,2p_L(1-p_L)+\frac{n_R}{n}\,2p_R(1-p_R)$$

## Explanation

In the first example the cut between $2$ and $4$, at $3.0$, perfectly separates the labels so its score is $0$. If all feature values are identical there is nothing to cut and `None` is returned.
