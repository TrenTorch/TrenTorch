---
name: sheet-maximum-points-from-cards
title: 'Maximum Points From Cards'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
theory: taking-cards-from-the-ends
---

## Statement

Cards lie in a row, and `points[i]` is the value of card `i`. In each of `k` steps you take **one card from either the left end or the right end**. Return the **maximum total** you can reach.

For `points = [1, 2, 3, 4, 5, 6, 1]` and `k = 3` the answer is `12` (the cards `1`, `6`, `5`).

### Examples

**Example 1**

Input:

```python
max_points([1, 2, 3, 4, 5, 6, 1], 3)
```

Output:

```text
12
```

**Example 2**

Input:

```python
max_points([2, 2, 2], 2)
```

Output:

```text
4
```

### Constraints

- `1 <= k <= len(points) <= 200000`
- `-10**4 <= points[i] <= 10**4`

## Explanation

`total - min_window` is the best sum of the cards taken from the ends. When `k == n` the window is empty and everything is taken.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                          | Variables                    |
| ---------------------------------------- | ---------------------------- |
| `n = len(points)`                        | `n = 7`                      |
| `size = n - k`                           | `size = 4`                   |
| `smallest = window`                      | `window = 10, smallest = 10` |
| `for i in range(size, n):`               | `i = 4`                      |
| `for i in range(size, n):`               | `window = 14, i = 5`         |
| `window += points[i] - points[i - size]` | `window = 18`                |
| `window += points[i] - points[i - size]` | `window = 16, i = 6`         |
| `return`                                 | `returned = 12`              |

### Complexity

- Time: O(n). The cards left in the middle form a window of fixed size `n - k` with the smallest sum.
- Space: O(1). A few numbers.
