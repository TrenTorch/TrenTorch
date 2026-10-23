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

## Theory

You do not need to match each parenthesis with its partner. Keep one number, the current **depth**: add `1` on `(`, subtract `1` on `)`, ignore everything else. The answer is the largest value the depth ever reaches.

This "running counter plus its maximum" is the simplest case of a more general idea: scan once, maintain a small summary of what you have seen. A full parenthesis checker with several bracket types needs a **stack**; for a single type a counter is enough.

## Explanation

`depth` goes up on `(` and down on `)`. After each increase, `best = max(best, depth)`. Characters other than parentheses do not matter.
