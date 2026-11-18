---
name: sheet-josephus
title: 'The Josephus Problem'
tags: [dsa-sheet, recursion, recursive-thinking]
difficulty: Advanced
theory: the-josephus-circle
---

## Statement

`n` people stand in a circle, numbered `1` to `n`. Starting at person `1`, count `k` people (counting person `1` as the first) and remove the person you land on; then start counting again from the next person still in the circle. Continue until one person is left. Return the **number** of the survivor.

For `n = 5` and `k = 2`: people `2`, `4`, `1`, `5` are removed in turn and person `3` survives.

The starter code simulates the circle by removing people from a list. It is correct but too slow for large `n` and `k`. Make it fast.

### Examples

**Example 1**

Input:

```python
josephus(5, 2)
```

Output:

```text
3
```

**Example 2**

Input:

```python
josephus(1, 7)
```

Output:

```text
1
```

### Constraints

- `1 <= n <= 2 * 10**5`
- `1 <= k <= 10**9`

## Explanation

`position` starts at `0` (one person, counting from 0). For every circle size `m` from 2 to `n`, `position = (position + k) % m`. The survivor is `position + 1` when numbering from 1.

### Complexity

- Time: O(n). The survivor of `m` people follows from the survivor of `m - 1` people, so one loop of `n - 1` steps.
- Space: O(1). One position.
