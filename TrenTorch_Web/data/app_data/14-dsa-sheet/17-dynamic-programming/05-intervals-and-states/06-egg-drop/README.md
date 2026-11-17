---
name: sheet-egg-drop
title: 'Egg Drop'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
theory: egg-drop
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

## Explanation

`reach[e]` is the number of floors checkable with the current number of drops. The update uses the old `reach[e - 1]`, so `e` runs downwards.

### Complexity

- Time: O(e * d). `d` is the answer (number of drops) and `e` the number of eggs: each drop updates how many floors `e` eggs can cover.
- Space: O(e). One row of the table.
