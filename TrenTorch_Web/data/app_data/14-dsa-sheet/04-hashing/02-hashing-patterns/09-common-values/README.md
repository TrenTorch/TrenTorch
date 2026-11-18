---
name: sheet-common-values
title: 'Common Values'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Beginner
theory: sets-for-comparing-two-lists
---

## Statement

Return a sorted list of the **different values** that appear in **both** `a` and `b`. The lists are not sorted and can contain repeats.

The starter code looks every value up in the other list with a linear search. It is correct but too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
common_values([1, 2, 2, 3], [2, 2, 3, 4])
```

Output:

```text
[2, 3]
```

**Example 2**

Input:

```python
common_values([1], [2])
```

Output:

```text
[]
```

### Constraints

- `0 <= len(a), len(b) <= 2 * 10**5`
- `-10**9 <= value <= 10**9`

## Explanation

`set(a) & set(b)` is every value present in both lists, each once. `sorted(...)` puts it in order.

### Complexity

- Time: O(n + m + t log t). Building the two sets is linear; `t` is the number of common values, which must be sorted for the output.
- Space: O(n + m). The two sets.
