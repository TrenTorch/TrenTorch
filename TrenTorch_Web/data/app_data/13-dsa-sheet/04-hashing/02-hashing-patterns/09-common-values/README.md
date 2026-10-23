---
name: sheet-common-values
title: 'Common Values'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Beginner
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

## Theory

Checking `x in b` on a **list** scans the list: `O(len(b))` per check. A **set** stores values by hash, so `x in some_set` is `O(1)` on average.

Turn one list into a set once (`O(n)`), then keep the values of the other list that are in it. Python's set operators make it a single expression: `set(a) & set(b)` is the **intersection**. `|` is union, `-` is difference, `^` is the values in exactly one.

Sets also remove repeats for free, which is why the answer is a list of _different_ values.

## Explanation

`set(a) & set(b)` is every value present in both lists, each once. `sorted(...)` puts it in order.
