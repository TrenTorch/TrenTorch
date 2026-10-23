---
name: sheet-egg-drop
title: 'Egg Drop'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
---

## Statement

A building has `floors` floors. There is a **critical floor** `F` (from `0` to `floors`): an egg dropped from any floor above `F` breaks, and from `F` or below it survives. You have `eggs` identical eggs (a surviving egg can be reused, a broken one is gone). Return the **minimum number of drops** that is enough to find `F` **in the worst case**.

For `eggs = 2` and `floors = 6` the answer is `3`.

The starter code tries every floor in every sub-problem. It is correct but too slow for tall buildings.

### Examples

**Example 1**

Input:

```python
egg_drop(2, 6)
```

Output:

```text
3
```

**Example 2**

Input:

```python
egg_drop(1, 2)
```

Output:

```text
2
```

### Constraints

- `0 <= eggs <= 100`
- `0 <= floors <= 100000`
- With no eggs and at least one floor, no search is possible: return `0`.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

The classic table `best[e][f]` (fewest drops with `e` eggs and `f` floors, trying every first floor) costs `O(e × f²)`. **Flip the question:** what is the **largest number of floors** `reach[m][e]` you can handle with `m` drops and `e` eggs? Drop an egg from some floor: if it **breaks**, `reach[m - 1][e - 1]` floors below can still be checked; if it **survives**, `reach[m - 1][e]` floors above can still be checked, plus the floor itself:

`reach[m][e] = reach[m - 1][e - 1] + reach[m - 1][e] + 1`.

Increase `m` until `reach[m][eggs] >= floors`. The number of drops needed is small (about `√(2 × floors)` for two eggs), so the loop is short. One array over `e` is enough, updated from high `e` to low.

## Explanation

`reach[e]` is the number of floors checkable with the current number of drops. The update uses the old `reach[e - 1]`, so `e` runs downwards.
