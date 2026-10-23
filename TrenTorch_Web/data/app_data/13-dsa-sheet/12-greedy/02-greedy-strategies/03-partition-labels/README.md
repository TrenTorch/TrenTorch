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

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

The first letter forces the first part to reach **at least as far as its last occurrence**. Every letter inside that range pulls the end further to **its** last occurrence. When the scan reaches the current end, all letters inside the part have their last occurrence inside it, so you can cut there. Then start again.

Precompute `last[ch]`, the index of the last occurrence of each letter. Scan with `end = max(end, last[s[i]])`; when `i == end`, record a part of size `end - start + 1`. `O(n)`. Cutting as early as possible gives the most parts.

## Explanation

`end` grows whenever a letter in the part occurs further right. A cut at `end` is valid because nothing in the part appears afterwards.
