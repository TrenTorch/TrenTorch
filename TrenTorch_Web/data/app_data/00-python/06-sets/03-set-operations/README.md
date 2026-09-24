---
name: python-sets-operations
title: "Set Operations: Union, Intersection, Difference, and Symmetric Difference"
tags: [python-set-operations]
difficulty: Intermediate
---

## Statement

Implement functions that combine sets and compare their contents using union, intersection, difference, and symmetric difference.

## Theory

For `A = {1, 2, 3}` and `B = {3, 4, 5}`:

| Operation | Symbol | Method | Result | Meaning |
|---|---|---|---|---|
| Union | `A \| B` | `A.union(B)` | `{1,2,3,4,5}` | everything in A or B |
| Intersection | `A & B` | `A.intersection(B)` | `{3}` | everything in both |
| Difference | `A - B` | `A.difference(B)` | `{1,2}` | in A but not B |
| Symmetric difference | `A ^ B` | `A.symmetric_difference(B)` | `{1,2,4,5}` | in exactly one |

All four produce a **new** set; neither operand changes. Difference is directional — `A - B` is generally not `B - A`.

**Relationship methods.** `issubset` (`<=`) tests whether every element of one set is in another; `issuperset` (`>=`) tests the reverse; `<`/`>` test *proper* (strict) subset/superset. `isdisjoint` tests whether two sets have no elements in common.

```python
{1, 2}.issubset({1, 2, 3})       # True
{1, 2}.isdisjoint({3, 4})         # True
```

**Where this matters later.** Set operations compare collections of features, vocabulary, IDs, or labels — intersection and difference are common when determining overlap between datasets.

## Explanation

`only_in_first` and `in_exactly_one` use `-` and `^` directly rather than looping and checking membership by hand, since the built-in operators already implement exactly "in A but not B" and "in exactly one of A and B" without any risk of getting the direction backwards. `relationship` returns `issubset`/`issuperset`/`isdisjoint` as a fixed-order tuple rather than three separate functions, since the spec asks for all three together and computing them independently (rather than deriving one from another) keeps each answer correct even for the edge case of two equal or two empty sets.
