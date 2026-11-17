---
name: sheet-top-characters
title: 'Most Frequent Characters'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
theory: counting-with-counter
---

## Statement

Return the `k` most frequent characters of `s` as a list of `[character, count]` pairs, most frequent first. When two characters have the same count, the one that comes first alphabetically goes first.

If `s` has fewer than `k` different characters, return all of them.

### Examples

**Example 1**

Input:

```python
top_characters('abracadabra', 2)
```

Output:

```text
[['a', 5], ['b', 2]]
```

`a` appears 5 times and `b` and `r` twice each; `b` is before `r`.

**Example 2**

Input:

```python
top_characters('zzyyx', 5)
```

Output:

```text
[['y', 2], ['z', 2], ['x', 1]]
```

Only three different characters exist, so all three are returned. `y` and `z` tie, so `y` is first.

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `0 <= k <= 100`
- `s` contains only lower-case letters.

## Explanation

Count once with `Counter`, then sort the (at most 26) items by `(-count, char)` and cut to `k`. Slicing with `[:k]` already handles `k` larger than the number of items and `k = 0`.

### Complexity

- Time: O(n + k log k). One pass to count the `n` characters, then a sort of the at most `k = 26` distinct letters, so O(n) overall.
- Space: O(k). The counter and the sorted list hold at most 26 entries.
