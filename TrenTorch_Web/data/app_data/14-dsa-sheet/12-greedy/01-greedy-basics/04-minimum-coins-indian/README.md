---
name: sheet-minimum-coins-indian
title: 'Fewest Coins and Notes'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Beginner
theory: fewest-coins-and-notes
---

## Statement

The available coins and notes are worth `1, 2, 5, 10, 20, 50, 100, 500, 2000`, with as many of each as you like. Return the **fewest coins and notes** that add up to exactly `amount`.

For `amount = 70` the answer is `2` (`50 + 20`); for `amount = 121` it is `3` (`100 + 20 + 1`).

### Examples

**Example 1**

Input:

```python
fewest_notes(70)
```

Output:

```text
2
```

**Example 2**

Input:

```python
fewest_notes(121)
```

Output:

```text
3
```

### Constraints

- `0 <= amount <= 10**12`

## Explanation

For each value, from the largest, `divmod` gives how many fit and the amount left. The counts add up to the answer.

### Complexity

- Time: O(1). Nine divisions, whatever the amount (this set of coins is one where taking the largest coin first is optimal).
- Space: O(1). A counter.
