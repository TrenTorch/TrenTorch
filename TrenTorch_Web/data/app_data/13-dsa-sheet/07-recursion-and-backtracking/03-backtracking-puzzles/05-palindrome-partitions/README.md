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

**Explanation:** For "aab", the palindromic partitions are ["a","a","b"] and ["aa","b"] because each piece reads the same forward and backward.

**Example 2**

Input:

```python
palindrome_partitions('a')
```

Output:

```text
[['a']]
```

**Explanation:** For "a", the only partition is ["a"] since a single character is a palindrome.

### Constraints

- `0 <= len(s) <= 14`
- `s` contains lower-case letters.

## Theory

At each step choose **where the next piece ends**. Try every end position `j` from the current start. If the piece `s[start:j]` is a palindrome, take it and solve the rest recursively; if it is not, skip it (that is the **pruning**: never extend a piece that is not a palindrome). When `start` reaches the end of the string, the pieces taken form one answer.

Testing a piece costs `O(length)`; the whole search is exponential in the worst case (a string like `"aaaa"` can be cut in `2^(n-1)` ways), which is why `n` is small.

## Explanation

`go(start, pieces)` appends a copy of `pieces` when `start == len(s)`. Otherwise for every end `j` it checks whether `s[start:j]` is a palindrome and, if so, recurses from `j`. The answer is sorted at the end so the order is exact.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line          | Variables                                                           |
| ------------------------ | ------------------------------------------------------------------- |
| `out = []`               | `out = []`                                                          |
| `def go(start, pieces):` | `go = <function palindrome_partitions.<locals>.go at 0x000001F4...` |
| `go(0, [])`              | `out = [['a', 'a', 'b'], ['aa', 'b']]`                              |
| `return`                 | `returned = [['a', 'a', 'b'], ['aa', 'b']]`                         |

### Complexity

- Time: O(n * 2^n) where n is the length of s.
- Extra space: O(n) where n is the length of s.
- The brute force takes O(n * 2^n) where n is the length of s.
