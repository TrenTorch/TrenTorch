---
name: sheet-partition-labels
title: 'Partition Labels'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Intermediate
---

## Statement

Cut `s` into as many **parts** as possible so that **each letter appears in at most one part**. Return the **sizes** of the parts, in order.

For `"ababcbacadefegdehijhklij"` the answer is `[9, 7, 8]`.

The starter code compares the letters on both sides of every cut position. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
partition_labels('ababcbacadefegdehijhklij')
```

Output:

```text
[9, 7, 8]
```

**Explanation:** A part ends when the index equals the farthest last position of any letter seen in it. That happens after 9 letters, then after 7, then after 8, giving [9, 7, 8].

**Example 2**

Input:

```python
partition_labels('eccbbbbdec')
```

Output:

```text
[10]
```

**Explanation:** The first letter e appears last at the very end of the string, so the first part has to stretch over all 10 letters.

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

The first letter forces the first part to reach **at least as far as its last occurrence**. Every letter inside that range pulls the end further to **its** last occurrence. When the scan reaches the current end, all letters inside the part have their last occurrence inside it, so you can cut there. Then start again.

Precompute `last[ch]`, the index of the last occurrence of each letter. Scan with `end = max(end, last[s[i]])`; when `i == end`, record a part of size `end - start + 1`. `O(n)`. Cutting as early as possible gives the most parts.

## Explanation

`end` grows whenever a letter in the part occurs further right. A cut at `end` is valid because nothing in the part appears afterwards.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                            | Variables                                                             |
| ------------------------------------------ | --------------------------------------------------------------------- |
| `last = {ch: i for i, ch in enumerate(s)}` | `last = {'a': 8, 'b': 5, 'c': 7, 'd': 14, 'e': 15, 'f': 11, 'g': ...` |
| `for i, ch in enumerate(s):`               | `sizes = [], start = 0, end = 8, i = 2, ch = 'a'`                     |
| `for i, ch in enumerate(s):`               | `i = 7, ch = 'c'`                                                     |
| `for i, ch in enumerate(s):`               | `sizes = [9], start = 9, end = 14, i = 10, ch = 'e'`                  |
| `for i, ch in enumerate(s):`               | `end = 15, i = 14, ch = 'd'`                                          |
| `for i, ch in enumerate(s):`               | `sizes = [9, 7], start = 16, end = 19, i = 17, ch = 'i'`              |
| `for i, ch in enumerate(s):`               | `end = 23, i = 20, ch = 'k'`                                          |
| `return`                                   | `returned = [9, 7, 8]`                                                |

### Complexity

- Time: O(n) where n is string length.
- Extra space: O(1) extra memory.
- The brute force takes O(n^2) where n is string length.
