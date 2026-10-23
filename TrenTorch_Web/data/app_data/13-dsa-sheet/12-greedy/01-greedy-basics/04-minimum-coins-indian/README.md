---
name: sheet-minimum-coins-indian
title: 'Fewest Coins and Notes'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Beginner
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

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

For this set of values, taking the **largest value that fits**, as many times as possible, and then going on with what is left, gives the fewest pieces. Use `divmod`: `count, amount = divmod(amount, value)` for each value from the largest.

Warning: greedy is **not** correct for every set of coin values. With coins `1, 3, 4` and amount `6`, greedy takes `4 + 1 + 1` (3 coins) while `3 + 3` needs only 2. A set of values for which greedy always works is called **canonical**; this one is. When it is not canonical, dynamic programming (later in the course) is the right tool.

## Explanation

For each value, from the largest, `divmod` gives how many fit and the amount left. The counts add up to the answer.
