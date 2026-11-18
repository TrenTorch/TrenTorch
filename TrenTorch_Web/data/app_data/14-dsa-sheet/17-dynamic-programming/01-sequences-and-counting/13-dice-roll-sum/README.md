---
name: sheet-dice-roll-sum
title: 'Dice Roll Sum'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
theory: dice-roll-sum
---

## Statement

You roll `dice` dice, each with faces numbered `1` to `faces`. Return the **number of ways** (different sequences of results) that the faces **add up to `target`**. Return the answer modulo `10**9 + 7`.

For `dice = 2`, `faces = 6` and `target = 7` the answer is `6`.

The starter code tries every face for every die. It is correct but too slow for many dice.

### Examples

**Example 1**

Input:

```python
dice_ways(2, 6, 7)
```

Output:

```text
6
```

**Example 2**

Input:

```python
dice_ways(1, 2, 3)
```

Output:

```text
0
```

### Constraints

- `0 <= dice <= 100`
- `1 <= faces <= 60`
- `0 <= target <= 1000`

## Explanation

`row[t]` is the number of ways for the current number of dice. `prefix` makes each window sum a subtraction of two prefix values.

### Complexity

- Time: O(dice * target). Prefix sums make each cell of a row O(1) instead of O(faces).
- Space: O(target). Two rows of the table.
