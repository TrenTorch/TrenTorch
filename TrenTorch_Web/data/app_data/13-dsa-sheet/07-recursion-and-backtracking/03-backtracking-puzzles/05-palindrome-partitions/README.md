---
name: sheet-palindrome-partitions
title: 'Palindrome Partitioning'
tags: [dsa-sheet, recursion, backtracking-puzzles]
difficulty: Intermediate
---

## Statement

Return every way to **cut `s` into pieces so that every piece is a palindrome** (reads the same both ways). Each way is a list of the pieces from left to right. List the ways sorted as lists of strings (compare the first piece, then the second, and so on).

For `"aab"`: `["a", "a", "b"]` and `["aa", "b"]`.

### Examples

**Example 1**

Input:

```python
palindrome_partitions('aab')
```

Output:

```text
[['a', 'a', 'b'], ['aa', 'b']]
```

**Example 2**

Input:

```python
palindrome_partitions('a')
```

Output:

```text
[['a']]
```

### Constraints

- `0 <= len(s) <= 14`
- `s` contains lower-case letters.

## Theory

At each step choose **where the next piece ends**. Try every end position `j` from the current start. If the piece `s[start:j]` is a palindrome, take it and solve the rest recursively; if it is not, skip it (that is the **pruning**: never extend a piece that is not a palindrome). When `start` reaches the end of the string, the pieces taken form one answer.

Testing a piece costs `O(length)`; the whole search is exponential in the worst case (a string like `"aaaa"` can be cut in `2^(n-1)` ways), which is why `n` is small.

## Explanation

`go(start, pieces)` appends a copy of `pieces` when `start == len(s)`. Otherwise for every end `j` it checks whether `s[start:j]` is a palindrome and, if so, recurses from `j`. The answer is sorted at the end so the order is exact.
