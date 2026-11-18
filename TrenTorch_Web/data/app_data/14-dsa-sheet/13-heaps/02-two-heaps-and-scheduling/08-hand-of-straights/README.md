---
name: sheet-hand-of-straights
title: 'Hand of Straights'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Intermediate
theory: the-smallest-card-must-start-a-group
---

## Statement

`hand[i]` is the number on card `i`. Return `True` if the cards can be split into groups of exactly `group_size` cards where each group holds **consecutive numbers** (`4, 5, 6` is a group of size 3).

For `hand = [1, 2, 3, 6, 2, 3, 4, 7, 8]` and `group_size = 3` the answer is `True` (`[1, 2, 3]`, `[2, 3, 4]`, `[6, 7, 8]`).

### Examples

**Example 1**

Input:

```python
is_n_straight_hand([1, 2, 3, 6, 2, 3, 4, 7, 8], 3)
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_n_straight_hand([1, 2, 3, 4, 5], 4)
```

Output:

```text
False
```

### Constraints

- `0 <= len(hand) <= 100000`
- `1 <= group_size <= 100000`
- `0 <= hand[i] <= 10**9`

## Explanation

The heap top is always the smallest number that still has cards. `count[x] -= 1` for each card of the group; a missing one ends the check.

### Complexity

- Time: O(n log n). A heap gives the smallest remaining card, and every card is counted down once.
- Space: O(n). The counts and the heap.
