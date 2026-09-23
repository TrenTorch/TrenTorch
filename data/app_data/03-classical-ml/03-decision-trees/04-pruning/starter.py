import numpy as np


def build_tree_pre_pruned(
    input: np.ndarray,
    labels: np.ndarray,
    max_depth: int,
    min_samples_leaf: int = 1,
) -> dict:
    """
    Like 03-best-split-minimal-tree's build_tree, with one more stopping
    rule: don't take a split if either resulting child would end up
    with fewer than min_samples_leaf samples.

    Every returned node (leaf or split) also carries a "default" field:
    the majority class of the training labels that reached this node,
    used later by prune_tree() as a fallback when no validation sample
    reaches a given node.
    """
    # TODO: Compute this node's majority class as `default`.
    # Stop conditions for a leaf (same as before, plus the new one):
    #   max_depth == 0, fewer than 2 samples, the node is already pure,
    #   find_best_split() finds nothing, OR the best split would leave
    #   a child with fewer than min_samples_leaf samples.
    # Otherwise recurse on both children with max_depth - 1.
    pass


def prune_tree(tree: dict, input_val: np.ndarray, labels_val: np.ndarray) -> dict:
    """
    Reduced-error post-pruning: given an already-built tree and a held-
    out validation set, walk the tree bottom-up. At each internal node,
    compare the validation error the subtree actually makes against the
    validation error a single leaf (predicting the majority class among
    the validation samples that reach this node) would make. Replace
    the subtree with that leaf whenever it does not increase error.

    Returns a new tree; the input tree is not mutated.
    """
    # TODO: If tree is a leaf, return it unchanged.
    # Otherwise: route input_val/labels_val to left/right by
    # tree["feature"]/tree["threshold"], recursively prune each side
    # first (bottom-up), then compare:
    #   - the recursively-pruned subtree's validation error
    #   - a single leaf's error, predicting the majority class of
    #     labels_val reaching this node (fall back to tree["default"]
    #     if no validation samples reach it)
    # Return the leaf if its error is <= the subtree's, else the
    # (already partially pruned) subtree.
    pass
