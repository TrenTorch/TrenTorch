---
name: decision-trees-pruning
title: Pruning (pre-pruning, post-pruning)
tags: [classical-ml, decision-trees, regularization]
difficulty: Intermediate
---

## Statement

Implement two functions:

```python
def build_tree_pre_pruned(
    input: np.ndarray, labels: np.ndarray, max_depth: int, min_samples_leaf: int = 1
) -> dict:
    """Like build_tree, plus: never take a split that leaves a child
    with fewer than min_samples_leaf samples. Every node also carries
    a "default" field: the majority class of training labels at that
    node."""

def prune_tree(tree: dict, input_val: np.ndarray, labels_val: np.ndarray) -> dict:
    """Reduced-error post-pruning against a held-out validation set."""
```

- `build_tree_pre_pruned` reuses `03-best-split-minimal-tree`'s `find_best_split` and stopping logic, with `min_samples_leaf` as one more stopping rule.
- `prune_tree` never mutates the tree it's given, it returns a new (possibly smaller) tree.

## Theory

`03-best-split-minimal-tree`'s `max_depth` is one way to stop a tree from growing too large, this is **pre-pruning**: decide, before or during construction, that a node shouldn't split further. `min_samples_leaf` is a second, independent pre-pruning rule: a split that would leave a child with only one or two samples is usually fitting noise in those specific samples, not a real pattern, refuse it even if it technically has positive information gain.

**Post-pruning** takes the opposite approach: build the tree as large as you like first, on the training set, then simplify it afterward using data the tree never saw during construction, a held-out validation set. The specific method here is **reduced-error pruning**: for every internal node, starting from the bottom of the tree and working up, ask "if I replaced this entire subtree with a single leaf, would validation accuracy get worse?" If not, replace it, a subtree that isn't earning its keep on unseen data.

```text
build_tree_pre_pruned(train)         # pre-pruning: some splits never happen
        ↓
   (possibly still overgrown tree)
        ↓
prune_tree(tree, validation)         # post-pruning: some splits get removed after the fact
```

Why bother with both when either alone limits overfitting? Pre-pruning is greedy and can stop too early, a split with zero gain right now might still enable a very good split one level deeper (the same limitation `03-best-split-minimal-tree`'s Theory names for greedy search generally). Post-pruning doesn't have that problem, since the full subtree already exists when the pruning decision is made, it can see whether the _combination_ of splits helped, not just the first one in isolation.

## Explanation

`build_tree_pre_pruned` computes `default`, this node's training-label majority class, before checking any stopping condition, every node needs it regardless of whether it ends up a leaf or a split (an internal node stores it so `prune_tree` can fall back to it later if no validation sample happens to reach that node). The one new stopping check, `left_mask.sum() < min_samples_leaf or (~left_mask).sum() < min_samples_leaf`, sits after `find_best_split` succeeds but before actually recursing, a split that satisfies information gain but violates `min_samples_leaf` is treated the same as no split being found at all.

`prune_tree` recurses into `left`/`right` _first_, using `tree["feature"]`/`tree["threshold"]` to route `input_val`/`labels_val` the same way `predict_tree` would, this is what makes it bottom-up: by the time a node compares itself against a leaf, its children have already been pruned as much as they're going to be. `candidate = {**tree, "left": ..., "right": ...}` keeps this node's own `feature`/`threshold`/`default` but swaps in the pruned children.

The comparison itself is `leaf_error <= subtree_error`, note `<=`, not `<`: when pruning doesn't help but doesn't hurt either, prefer the simpler leaf, a tree with fewer nodes that performs identically on validation data generalizes at least as well and is cheaper to evaluate. `leaf_prediction = _majority_class(labels_val, default=tree["default"])` uses the validation samples that reached this node when there are any, and the training-time `default` when there are none, a node no validation sample ever visits can't have its pruning decision informed by validation data, so it falls back to what the training data already said.
