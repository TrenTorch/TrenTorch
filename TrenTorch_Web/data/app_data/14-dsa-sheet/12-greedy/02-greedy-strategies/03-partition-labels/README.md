---
name: sheet-partition-labels
title: 'Partition Labels'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Intermediate
theory: partition-labels
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

**Example 2**

Input:

```python
partition_labels('eccbbbbdec')
```

Output:

```text
[10]
```

### Constraints

- `0 <= len(s) <= 200000`
- Lower-case letters.

## Explanation

`end` grows whenever a letter in the part occurs further right. A cut at `end` is valid because nothing in the part appears afterwards.

### Complexity

- Time: O(n). One pass to find the last position of each letter and one to cut the string.
- Space: O(k). The last-position map has one entry per letter, `k` <= 26.
