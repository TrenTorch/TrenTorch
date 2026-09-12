---
name: decision-trees-information-gain
title: Information Gain for a split
tags: [classical-ml, decision-trees, splitting-criteria]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Once a node is mixed, a tree must compare proposed partitions. A useful split leaves its children more label-consistent than their parent; a useless split merely moves the same mixture around. Information gain measures that reduction while ensuring a tiny child cannot count as much as a large one.

### From theory to code

Implement `information_gain(parent_labels, left_labels, right_labels)` using the existing `gini_impurity` helper and a child-size-weighted average.

### Constraints

- `left_labels` and `right_labels` partition `parent_labels`.
- Return a Python `float` gain.
- Weight each child impurity by its size divided by `parent_labels.size`.
- Empty children remain valid because `gini_impurity` returns `0.0` for them.
- Reuse `gini_impurity`; do not reimplement its class counting.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Start from the parent's impurity, then ask what impurity remains after routing samples into children.

</details>

<details><summary>Hint 2</summary>

The remaining impurity is not an even average: multiply each child's impurity by `child.size / parent.size` first.

</details>

## Theory

### The simple version

Information gain is the cleanliness a split buys. A perfect split creates pure children, so it preserves none of the parent's confusion. Splitting off no examples changes nothing and gains nothing.

### The formula

```text
n = parent_labels.size
child_impurity = (left_labels.size / n) * gini(left_labels)
               + (right_labels.size / n) * gini(right_labels)
gain = gini(parent_labels) - child_impurity
```

### How PyTorch actually implements this

Context only, untested by your submission: Gini-based greedy split scoring is normally supplied by tree libraries rather than `torch.nn`; this code spells out the criterion directly.

## Explanation

`n_samples = parent_labels.size` is the common denominator for both child weights. `weighted_child_impurity` calls `gini_impurity` on each child and multiplies it by that child's share of the parent, rather than averaging the two values equally. The return line subtracts this remaining impurity from the parent's value, producing zero for an unchanged partition and positive gain for an improving split.
