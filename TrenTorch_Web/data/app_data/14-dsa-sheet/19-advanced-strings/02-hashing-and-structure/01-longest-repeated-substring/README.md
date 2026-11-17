---
name: sheet-longest-repeated-substring
title: 'Longest Repeated Substring'
tags: [dsa-sheet, advanced-strings, hashing-and-structure]
difficulty: Mastery
theory: binary-search-on-the-length-longest-repeated-substring
---

## Statement

Return the length of the **longest substring that occurs at least twice** in `s` (the two occurrences may overlap). Return `0` if every letter occurs once.

For `"banana"` the answer is `3` (`"ana"`).

The starter code builds every substring of every length. It is correct but too slow for long strings.

### Examples

**Example 1**

Input:

```python
longest_repeated_length('banana')
```

Output:

```text
3
```

**Example 2**

Input:

```python
longest_repeated_length('abcd')
```

Output:

```text
0
```

### Constraints

- `0 <= len(s) <= 20000`
- Lower-case letters.

## Explanation

Build a suffix automaton of `s`: a small graph whose paths from the start are exactly the substrings of `s`. Each state stands for a group of substrings that end at the same set of positions; it records the longest of them (`length`), a `link` to the state of the longest suffix that ends at more positions, and a count `occ` of how often those substrings occur.

While building, every new letter creates a state with `occ = 1` (one new ending position); copies made to split a state start with `occ = 0`. Then add each state's count to its `link` in order of decreasing `length`, so a state ends up with the number of ending positions of everything it represents. A substring that occurs twice or more belongs to a state with `occ >= 2`, so the answer is the largest `length` among them.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                     | Variables                                                                                                                                                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `nxt = [{}]`                        | `nxt = [{}]`                                                                                                                                                                                                                |
| `length.append(length[last] + 1)`   | `nxt = [{'b': 1}, {}, {}], link = [-1, 0, 0], length = [0, 1, 2], occ = [0, 1], last = 1, ch = 'a', cur = 2, p = -1`                                                                                                        |
| `for ch in s:`                      | `nxt = [{'b': 1, 'a': 2, 'n': 3}, {'a': 2}, {'n': 3}, {}], link = [-1, 0, 0, 0], length = [0, 1, 2, 3], occ = [0, 1, 1, 1], last = 3, cur = 3`                                                                              |
| `for ch in s:`                      | `nxt = [{'b': 1, 'a': 5, 'n': 3}, {'a': 2}, {'n': 3}, {'a': 4}, ..., link = [-1, 0, 5, 0, 5, 0], length = [0, 1, 2, 3, 4, 1], occ = [0, 1, 1, 1, 1, 0], last = 4, ch = 'n', cur = 4, q = 2, clone = 5`                      |
| `link.append(0)`                    | `nxt = [{'b': 1, 'a': 5, 'n': 7}, {'a': 2}, {'n': 3}, {'a': 4}, ..., link = [-1, 0, 5, 7, 5, 0, 7, 0, 0], length = [0, 1, 2, 3, 4, 1, 5, 2], occ = [0, 1, 1, 1, 1, 0, 1, 0], last = 6, ch = 'a', cur = 8, q = 3, clone = 7` |
| `by_length[length[v]].append(v)`    | `link = [-1, 0, 5, 7, 9, 0, 7, 0, 9, 5], length = [0, 1, 2, 3, 4, 1, 5, 2, 6, 3], occ = [0, 1, 1, 1, 1, 0, 1, 0, 1, 0], last = 8, p = 0, q = 4, clone = 9, by_length = [[], [1], [2], [3], [], [], []], v = 3`              |
| `for size in range(len(s), 0, -1):` | `occ = [0, 1, 1, 1, 1, 0, 1, 1, 1, 1], by_length = [[], [1, 5], [2, 7], [3, 9], [4], [6], [8]], v = 6, best = 0, size = 4`                                                                                                  |
| `return`                            | `returned = 3`                                                                                                                                                                                                              |

### Complexity

- Time: O(n * sigma). A suffix automaton is built online in linear time; every state knows how many times its substrings occur, so the longest substring with two or more occurrences is a maximum over the states (`sigma` = alphabet size, since transitions are dictionaries).
- Space: O(n * sigma). At most `2n` states with their transitions.
