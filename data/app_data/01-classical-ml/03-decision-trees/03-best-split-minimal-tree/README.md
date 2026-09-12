---
name: decision-trees-best-split-minimal-tree
title: Decision Tree best split (assemble a minimal tree)
tags: [classical-ml, decision-trees, tree-building]
difficulty: Advanced
---

## Statement

Implement three functions:

```python
def find_best_split(input: np.ndarray, labels: np.ndarray) -> tuple[int, float, float] | None:
    """Search every feature/threshold, return (feature, threshold, gain) or None."""

def build_tree(input: np.ndarray, labels: np.ndarray, max_depth: int) -> dict:
    """Recursively assemble a tree using find_best_split() at every node."""

def predict_tree(tree: dict, input: np.ndarray) -> np.ndarray:
    """Walk the tree from root to leaf for every row of input."""
```

- `find_best_split` tries every feature, and for each feature every midpoint between consecutive sorted unique values as a candidate threshold, `input[:, feature] <= threshold` vs. `> threshold`. A midpoint between two adjacent present values always puts at least one sample on each side, by construction.
- `build_tree` stops and returns a leaf when `max_depth` reaches `0`, fewer than 2 samples remain, the node is already pure (`01-gini-impurity`'s `gini_impurity` is `0`), or `find_best_split` returns `None` (no split improves anything).
- A leaf's prediction is the majority class among its samples.
- Reuse `01-gini-impurity` and `02-information-gain` rather than reimplementing them.

## Theory

`02-information-gain` scores one candidate split. Building an actual tree means searching over _every_ candidate split at a node, keeping the best one, then repeating the whole process independently on each of the two resulting children, recursively, until some stopping condition says "this node is good enough, make it a leaf."

The candidate thresholds themselves come from the data: for a continuous feature, the only thresholds that can possibly change which samples land on which side are the midpoints between consecutive distinct values that actually occur, `01-gini-impurity` and `02-information-gain` never change value between two data points, only at the boundary between them.

This is genuinely not a vectorizable operation the way most of this curriculum has been so far. A tree's structure depends on data-dependent branching decisions made one node at a time, there's no single matrix expression that "is" a decision tree the way `input @ weight.T` "is" a linear layer. Real `scikit-learn` builds trees the same recursive way internally (in compiled Cython for speed, not because the algorithm itself vectorizes), which is exactly why `DecisionTreeClassifier` has no NumPy/PyTorch equivalent one-liner, tree construction is a search-and-recurse algorithm, not a tensor operation.

`max_depth` exists because an unbounded tree will keep splitting until every leaf is perfectly pure, including leaves with a single sample, which memorizes the training data instead of learning a generalizable pattern. `04-pruning`, the next question in this track, is the more principled version of controlling exactly this.

A real, well-known limitation falls straight out of this greedy design: true XOR, where the label is 1 in exactly two diagonally-opposite quadrants and 0 in the other two, gives _every_ single candidate split exactly zero information gain at the root. Splitting on either feature alone always produces two children that are each perfectly 50/50 mixed, no better than not splitting at all. A greedy, one-step-at-a-time search like this one never takes that first, individually-useless split, even though two splits together would separate the data perfectly. This isn't a bug, it's a genuine blind spot of greedy top-down induction, and it's exactly why ensembles of many differently-built trees (`Ensembles`, the next track) tend to outperform any single greedy tree on data with this kind of interaction structure.

## Explanation

`find_best_split` loops over `range(n_features)`, and for each one, `np.unique(input[:, feature])` gets the sorted distinct values actually present, `(values[:-1] + values[1:]) / 2` is every consecutive midpoint at once, vectorized, even though the surrounding search is a Python loop. No separate check for an empty child is needed, a midpoint between two adjacent present values guarantees at least one sample lands on each side.

`build_tree`'s base case returns `{"leaf": True, "prediction": _majority_class(labels)}`, the majority class is found via `np.unique(labels, return_counts=True)` and taking the value with the largest count, same primitive `01-gini-impurity` already uses for counting. The recursive case builds the two child subtrees on `max_depth - 1`, so depth is enforced by counting down to `0`, not by tracking depth upward.

`predict_tree` walks one sample at a time: at a split node, compare that sample's value at `node["feature"]` against `node["threshold"]` to decide left or right, repeat until `node["leaf"]` is `True`. This mirrors exactly how `build_tree` decided each split in the first place, a sample takes the same path at prediction time that its training-time siblings took at training time.
