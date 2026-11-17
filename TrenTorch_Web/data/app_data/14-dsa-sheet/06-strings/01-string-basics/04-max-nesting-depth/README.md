---
name: sheet-max-nesting-depth
title: 'Maximum Nesting Depth'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: keeping-a-running-number
---

## Statement

`s` is a valid string of parentheses mixed with other characters (every `(` has a matching `)`). Return the **maximum nesting depth**: the largest number of `(` that are open at the same time.

### Examples

**Example 1**

Input:

```python
max_nesting_depth('(1+(2*3)+((8)/4))+1')
```

Output:

```text
3
```

**Example 2**

Input:

```python
max_nesting_depth('abc')
```

Output:

```text
0
```

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- The parentheses in `s` are balanced and correctly ordered.

## Explanation

`depth` goes up on `(` and down on `)`. After each increase, `best = max(best, depth)`. Characters other than parentheses do not matter.

### Complexity

- Time: O(n). One pass keeping the current depth.
- Space: O(1). Two counters.
