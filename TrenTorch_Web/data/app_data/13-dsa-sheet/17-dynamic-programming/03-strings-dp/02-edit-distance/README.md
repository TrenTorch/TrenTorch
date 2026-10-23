---
name: sheet-edit-distance
title: 'Edit Distance'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Advanced
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

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

This is the **Levenshtein distance**. **State:** `dist(i, j)`, the fewest operations to turn the first `i` characters of `a` into the first `j` of `b`. **Transition:** if `a[i - 1] == b[j - 1]` nothing is needed for the last character: `dist(i, j) = dist(i - 1, j - 1)`. Otherwise try the three operations and take the best:

- replace: `1 + dist(i - 1, j - 1)`,
- delete a character of `a`: `1 + dist(i - 1, j)`,
- insert a character into `a`: `1 + dist(i, j - 1)`.

**Base cases:** `dist(i, 0) = i` (delete everything) and `dist(0, j) = j` (insert everything). `O(len(a) × len(b))`, rolling rows for memory.

## Explanation

The first entry of every row is `i` (deleting `i` characters). `cur[j - 1] + 1` is an insertion, `prev[j] + 1` a deletion, `prev[j - 1] + 1` a replacement.
