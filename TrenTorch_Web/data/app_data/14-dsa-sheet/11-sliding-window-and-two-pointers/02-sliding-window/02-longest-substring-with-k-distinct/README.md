---
name: sheet-longest-substring-with-k-distinct
title: 'Longest Substring With K Distinct Characters'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
theory: at-most-k-different-letters
---

## Statement

Return the length of the **longest substring** of `s` that has **at most `k` different characters**.

For `s = "eceba"` and `k = 2` the answer is `3` (`"ece"`).

The starter code tries every start. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_k_distinct('eceba', 2)
```

Output:

```text
3
```

**Example 2**

Input:

```python
longest_k_distinct('aa', 1)
```

Output:

```text
2
```

### Constraints

- `0 <= len(s) <= 200000`
- `0 <= k <= 26`
- `s` contains lower-case letters.

## Explanation

`count` maps each character in the window to how many times it appears. A key whose count drops to zero is deleted so `len(count)` stays the number of different characters.

### Complexity

- Time: O(n). Each index enters and leaves the window once.
- Space: O(k). The count map has at most `k + 1` entries.
