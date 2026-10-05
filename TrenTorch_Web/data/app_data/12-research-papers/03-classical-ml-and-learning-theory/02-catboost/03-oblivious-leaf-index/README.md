---
name: research-catboost-oblivious-leaf
title: 'CatBoost: Oblivious Tree Leaf Index'
tags: [research-papers, classical-ml, boosting, catboost]
difficulty: Beginner
---

## Statement

### The problem, from first principles

CatBoost uses oblivious trees: every node on the same level applies the same split. So a sample's leaf is fully determined by the outcome of each level's split, which is a binary code.

### From theory to code

Implement `oblivious_leaf_index(bits)`, converting the level outcomes into an integer leaf index.

### Constraints

- Bit `k` has weight `2 ** k`.

### Hints

<details>
<summary>Hint 1</summary>

Sum each bit times its power of two.

</details>

## Theory

### The simple version

Because the tree is symmetric, the leaf index is just the binary number formed by the split outcomes. That makes prediction a table lookup, which is fast.

### The formula

$$\text{leaf} = \sum_{k=0}^{d-1} b_k\,2^{k}$$

### How NumPy/PyTorch actually implements this

CatBoost's inference code evaluates the split conditions in a loop and builds the same index.

## Explanation

Each level contributes one bit, so a depth-`d` oblivious tree has `2^d` leaves indexed by these bits.
