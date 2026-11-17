---
name: sheet-suffix-array
title: 'Suffix Array'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Mastery
theory: prefix-doubling
---

## Statement

The **suffix array** of `s` lists the starting positions of all its suffixes, in the **dictionary order of the suffixes**. For `"banana"` the suffixes sorted are `a, ana, anana, banana, na, nana` (starting at 5, 3, 1, 0, 4, 2), so the answer is `[5, 3, 1, 0, 4, 2]`.

### Examples

**Example 1**

Input:

```python
suffix_array('banana')
```

Output:

```text
[5, 3, 1, 0, 4, 2]
```

**Example 2**

Input:

```python
suffix_array('aaaa')
```

Output:

```text
[3, 2, 1, 0]
```

### Constraints

- `0 <= len(s) <= 10000`
- Lower-case letters.

## Explanation

Prefix doubling. Treat each suffix as a cyclic shift of `s + sentinel` (the sentinel is smaller than every letter), and give every shift a class number by its first `2^k` letters. To sort by the first `2^(k+1)` letters, sort by the second half and then, stably, by the first half; both halves are class numbers, so counting sort does it in O(n). Equal pairs get the same new class. After `log2(n)` rounds all shifts are in their final order; dropping the sentinel's own shift gives the suffix array.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                                          | Variables                                                                                                                                                                                                    |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `text = [ord(ch) + 1 for ch in s] + [0]  # 0 is the sentinel, smaller than every letter` | `text = [99, 98, 111, 98, 111, 98, 0]`                                                                                                                                                                       |
| `for i in range(1, size):`                                                               | `n = 7, size = 112, order = [0, 0, 0, 0, 0, 0, 0], cls = [0, 0, 0, 0, 0, 0, 0], count = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,..., v = 0, i = 26`                                         |
| `for i in range(1, size):`                                                               | `i = 82`                                                                                                                                                                                                     |
| `cls[order[i]] = classes - 1`                                                            | `order = [6, 1, 3, 5, 0, 2, 4], cls = [2, 1, 3, 1, 0, 1, 0], count = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,..., i = 5, classes = 4`                                                       |
| `classes += 1`                                                                           | `order = [6, 5, 1, 3, 0, 2, 4], cls = [2, 1, 3, 1, 3, 1, 0], count = [0, 1, 4, 5], i = 2, classes = 3, shift = 1, by_second = [5, 0, 2, 4, 6, 1, 3], c = 1, new_cls = [0, 0, 0, 0, 0, 1, 0], a = 1, b = 5`   |
| `c = cls[by_second[i]]`                                                                  | `order = [6, 5, 1, 1, 0, 2, 2], cls = [3, 2, 4, 2, 4, 1, 0], count = [1, 1, 3, 4, 6], classes = 5, shift = 2, by_second = [4, 3, 6, 1, 5, 0, 2], c = 0, new_cls = [3, 2, 4, 2, 4, 1, 0], a = 4, b = 2`       |
| `for i in range(1, classes):`                                                            | `order = [6, 5, 3, 1, 0, 4, 2], cls = [4, 3, 6, 2, 5, 1, 0], count = [1, 2, 1, 1, 1, 1, 1], classes = 7, shift = 4, by_second = [2, 1, 6, 4, 3, 0, 5], c = 4, new_cls = [4, 3, 6, 2, 5, 1, 0], a = 2, b = 4` |
| `return`                                                                                 | `returned = [5, 3, 1, 0, 4, 2]`                                                                                                                                                                              |

### Complexity

- Time: O(n log n). Prefix doubling: after each of the `log n` rounds the suffixes are ordered by their first `2^k` letters, and each round is two counting sorts of O(n). (A linear-time algorithm, SA-IS, exists but is much longer).
- Space: O(n). The order, class and counting arrays.
