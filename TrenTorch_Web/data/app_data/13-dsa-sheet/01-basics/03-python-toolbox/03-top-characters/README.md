---
name: sheet-top-characters
title: 'Most Frequent Characters'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Beginner
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

- `0 <= len(s) <= 10**6`
- `0 <= k <= 100`
- `s` contains only lower-case letters.

## Theory

`Counter(s).most_common(k)` returns the `k` biggest counts, but when counts tie it keeps the order in which the characters were **first seen**, not alphabetical. It is a common trap.

To control ties, sort the `(character, count)` pairs yourself with a tuple key `(-count, character)`: biggest count first, then the smaller character. The number of different characters is small (26 here), so sorting them is cheap; counting is the `O(n)` part.

## Explanation

Count once with `Counter`, then sort the (at most 26) items by `(-count, char)` and cut to `k`. Slicing with `[:k]` already handles `k` larger than the number of items and `k = 0`.
