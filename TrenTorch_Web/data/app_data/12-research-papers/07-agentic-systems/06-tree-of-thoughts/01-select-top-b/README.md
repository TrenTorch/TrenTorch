---
name: research-tot-select-top-b
title: 'Tree of Thoughts: Keeping the Best Thoughts'
tags: [research-papers, agents, search, reasoning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Tree of Thoughts (Yao et al., 2023) explores reasoning as a search. At each depth it generates several candidate thoughts, scores them with the model, and keeps only the best few. Keeping the top b states is that beam step.

### From theory to code

Implement `select_top_b(states, scores, b)`, returning the b best states in order.

### Constraints

- Higher scores are better.

### Hints

<details>
<summary>Hint 1</summary>

Sort the indices by score descending, then take the first b states.

</details>

## Theory

### The simple version

The beam limits the search cost: without it the tree would grow exponentially with depth. Selecting by value keeps the promising branches.

### The formula

$$\mathcal{B}_{t+1} = \text{top}_b\big\{ s' : s' \in \text{expand}(s),\; s \in \mathcal{B}_t \big\}$$

### How NumPy/PyTorch actually implements this

Tree-search agent frameworks implement a beam over model-scored candidates with this selection.

## Explanation

Sorting the indices rather than the states keeps the code correct when states are not comparable.
