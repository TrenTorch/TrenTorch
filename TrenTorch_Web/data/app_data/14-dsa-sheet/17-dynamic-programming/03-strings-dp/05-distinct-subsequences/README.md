---
name: sheet-distinct-subsequences
title: 'Distinct Subsequences'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Advanced
theory: counting-subsequences
---

## Statement

Return the **number of ways** to pick characters of `s` (keeping their order) that spell `t`. Different choices of positions count as different ways. Return the answer modulo `10**9 + 7`.

For `s = "rabbbit"` and `t = "rabbit"` the answer is `3`.

The starter code is a plain recursion. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
num_distinct('rabbbit', 'rabbit')
```

Output:

```text
3
```

**Example 2**

Input:

```python
num_distinct('babgbag', 'bag')
```

Output:

```text
5
```

### Constraints

- `0 <= len(s) <= 2000`
- `0 <= len(t) <= 500`
- Lower-case letters.

## Explanation

`row[j]` is the number of ways to spell `t[:j]` with the characters seen so far. Iterating `j` downwards uses the previous row's `row[j - 1]`.

### Complexity

- Time: O(n * m). Every cell of the table is computed once, in O(1).
- Space: O(m). One row of the table (`n` = len(s), `m` = len(t)).
