---
name: decision-trees-pruning
title: Pruning (pre-pruning, post-pruning)
tags: [classical-ml, decision-trees, regularization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Growing every positive-gain split can create branches that memorize a few training examples. Pre-pruning rejects suspiciously small children while building; post-pruning removes branches that do not earn their complexity on held-out data. This exercise implements both controls around the tree from `03-best-split-minimal-tree`.

### From theory to code

Implement `build_tree_pre_pruned` and `prune_tree`. Theory explains the extra child-size condition and the bottom-up comparison between a recursively pruned subtree and one fallback leaf.

### Constraints

- `build_tree_pre_pruned` follows the previous tree's depth, sample-count, purity, and no-split stop rules.
- Reject a candidate split when either child has fewer than `min_samples_leaf` samples.
- Every returned node stores the training-label majority class in `default`.
- `prune_tree` returns a new tree and never mutates its `tree` argument.
- Route validation data by each node's stored `feature` and inclusive `threshold` before recursing.
- Replace a subtree when the fallback leaf's validation error is less than or equal to the subtree error; use `default` if no validation label reaches a node.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Compute the node's majority class before any early return: both leaves and split nodes need it.

</details>

<details><summary>Hint 2</summary>

Prune children first. Only then does a parent compare its best already-pruned subtree with one leaf.

</details>

## Theory

### The simple version

Pre-pruning refuses to grow a branch supported by too little evidence. Reduced-error pruning grows the tree first, then asks validation data whether each completed branch predicts better than its simplest possible replacement. When there is a tie, keep the simpler tree.

### The formula

For the selected split mask `L`, construction accepts it only when:

```text
L.sum() >= min_samples_leaf
(~L).sum() >= min_samples_leaf
```

At an internal validation node, first create recursively pruned children. Then compare:

```text
subtree_error = sum(predict_tree(candidate, input_val) != labels_val)
leaf_prediction = majority_class(labels_val, default=tree["default"])
leaf_error = sum(leaf_prediction != labels_val)
```

Return the leaf when `leaf_error <= subtree_error`; otherwise retain `candidate`.

### How PyTorch actually implements this

Context only, untested by your submission: pruning is a tree-induction policy, not a core `torch.nn` layer. Libraries such as scikit-learn expose tree-complexity controls, while this exercise makes the decisions explicit.

## Explanation

`default = _majority_class(labels)` happens before the build stop conditions, so every leaf and split dictionary includes a safe training fallback. After `find_best_split`, `left_mask.sum()` and `(~left_mask).sum()` implement the new pre-pruning rule; a violating split returns the same default leaf as no split.

`prune_tree` immediately returns an existing leaf. For a split it derives `left_mask` from the stored node fields, recursively prunes each routed validation subset, and assembles `candidate` with `{**tree, "left": ..., "right": ...}` rather than changing `tree`. It compares validation mistakes from `predict_tree(candidate, input_val)` against the validation-majority leaf. The inclusive tie condition makes pruning never worsen validation error while preferring fewer nodes.
