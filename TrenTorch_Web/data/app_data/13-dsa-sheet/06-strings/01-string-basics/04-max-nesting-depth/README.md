---
name: sheet-max-nesting-depth
title: 'Maximum Nesting Depth'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
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

**Explanation:** Three opening parentheses appear before any closing, so maximum simultaneous open count is 3.

**Example 2**

Input:

```python
max_nesting_depth('abc')
```

Output:

```text
0
```

**Explanation:** The string contains no parentheses, so depth never rises above 0.

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- The parentheses in `s` are balanced and correctly ordered.

## Theory

You do not need to match each parenthesis with its partner. Keep one number, the current **depth**: add `1` on `(`, subtract `1` on `)`, ignore everything else. The answer is the largest value the depth ever reaches.

This "running counter plus its maximum" is the simplest case of a more general idea: scan once, maintain a small summary of what you have seen. A full parenthesis checker with several bracket types needs a **stack**; for a single type a counter is enough.

## Explanation

`depth` goes up on `(` and down on `)`. After each increase, `best = max(best, depth)`. Characters other than parentheses do not matter.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line           | Variables                       |
| ------------------------- | ------------------------------- |
| `depth = best = 0`        | `depth = 0, best = 0`           |
| `for ch in s:`            | `depth = 1, best = 1, ch = '1'` |
| `best = max(best, depth)` | `depth = 2, best = 2, ch = '('` |
| `for ch in s:`            | `ch = ')'`                      |
| `depth += 1`              | `depth = 3, ch = '('`           |
| `depth -= 1`              | `depth = 2, best = 3, ch = ')'` |
| `depth -= 1`              | `depth = 1`                     |
| `return`                  | `returned = 3`                  |

### Complexity

- Time: O(n) time, n = length of s.
- Extra space: O(1) extra space.
- The brute force takes O(n^2) time, n = length of s.
