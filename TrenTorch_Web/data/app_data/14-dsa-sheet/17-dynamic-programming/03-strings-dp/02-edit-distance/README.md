---
name: sheet-edit-distance
title: 'Edit Distance'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Advanced
theory: edit-distance
---

## Statement

Return the **minimum number of operations** to turn the string `a` into `b`, where one operation is **inserting** a character, **deleting** a character or **replacing** a character.

For `a = "horse"` and `b = "ros"` the answer is `3` (`horse -> rorse -> rose -> ros`).

The starter code is a plain recursion. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
edit_distance('horse', 'ros')
```

Output:

```text
3
```

**Example 2**

Input:

```python
edit_distance('intention', 'execution')
```

Output:

```text
5
```

### Constraints

- `0 <= len(a), len(b) <= 800`
- Lower-case letters.

## Explanation

The first entry of every row is `i` (deleting `i` characters). `cur[j - 1] + 1` is an insertion, `prev[j] + 1` a deletion, `prev[j - 1] + 1` a replacement. Edit distance is the same in both directions, so the strings are swapped if needed to keep the rows short.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                      | Variables                                               |
| ---------------------------------------------------- | ------------------------------------------------------- |
| `prev = list(range(len(b) + 1))`                     | `prev = [0, 1, 2, 3]`                                   |
| `for j in range(1, len(b) + 1):`                     | `i = 1, cur = [1, 1, 2, 0], j = 3`                      |
| `cur[j] = 1 + min(prev[j - 1], prev[j], cur[j - 1])` | `prev = [1, 1, 2, 3], i = 2, cur = [2, 2, 0, 0], j = 1` |
| `cur = [i] + [0] * len(b)`                           | `prev = [2, 2, 1, 2], i = 3, cur = [3, 0, 0, 0], j = 3` |
| `cur[j] = 1 + min(prev[j - 1], prev[j], cur[j - 1])` | `cur = [3, 2, 2, 2]`                                    |
| `cur[j] = 1 + min(prev[j - 1], prev[j], cur[j - 1])` | `prev = [3, 2, 2, 2], i = 4, cur = [4, 3, 3, 0], j = 2` |
| `for j in range(1, len(b) + 1):`                     | `prev = [4, 3, 3, 2], i = 5, cur = [5, 0, 0, 0], j = 1` |
| `return`                                             | `returned = 3`                                          |

### Complexity

- Time: O(n * m). Every cell of the `n x m` table is computed once; subquadratic algorithms are not known for the general case.
- Space: O(min(n, m)). Two rows of the table, laid along the shorter string.
