---
name: sheet-hand-of-straights
title: 'Hand of Straights'
tags: [dsa-sheet, heaps, two-heaps-and-scheduling]
difficulty: Intermediate
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

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

Look at the **smallest** card that is left. Whatever happens, it must be the **start** of a group (no smaller card remains to precede it), so the group has to be `x, x + 1, ..., x + size - 1`. Remove one of each of those; if one of them is missing, the answer is `False`. Repeat with the new smallest card.

Keep the counts of each number in a dictionary and a min-heap of the distinct numbers to find the smallest. When the smallest number's count becomes 0, pop it. If the number of cards is not a multiple of `group_size`, the answer is `False` right away.

## Explanation

The heap top is always the smallest number that still has cards. `count[x] -= 1` for each card of the group; a missing one ends the check.
