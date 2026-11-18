---
name: sheet-longest-common-substring
title: 'Longest Common Substring'
tags: [dsa-sheet, dynamic-programming, strings-dp]
difficulty: Intermediate
theory: longest-common-substring
---

## Statement

A **substring** is a block of **consecutive** characters. Return the length of the **longest substring that appears in both `a` and `b`**.

For `a = "abcdxyz"` and `b = "xyzabcd"` the answer is `4` (`"abcd"`).

### Examples

**Example 1**

Input:

```python
longest_common_substring('abcdxyz', 'xyzabcd')
```

Output:

```text
4
```

**Example 2**

Input:

```python
longest_common_substring('zxabcdezy', 'yzabcdezx')
```

Output:

```text
6
```

### Constraints

- `0 <= len(a), len(b) <= 900`
- Lower-case letters.

## Explanation

A suffix automaton of `a` is a small graph that contains every substring of `a` as a path from the start state. It can be built in linear time and has at most `2 * len(a)` states, each with a `length` (the longest substring that ends there) and a `link` to the state of the longest proper suffix that is in a different class.

Walk through `b` letter by letter with the current state and the current match length. If the letter extends the match, follow that edge and add one. If not, follow `link`s until some state has the letter (the match length drops to that state's `length`), or restart from the start state with length 0. The longest length seen is the answer. Each step either moves forward or shortens the match, so the walk is linear.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line       | Variables                                                                                                                                                                |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `nxt = [{}]`          | `nxt = [{}]`                                                                                                                                                             |
| `cur = len(nxt)`      | `nxt = [{'a': 1}, {}], link = [-1, 0], length = [0, 1], last = 1, ch = 'b', cur = 2, p = -1`                                                                             |
| `p = last`            | `nxt = [{'a': 1, 'b': 2}, {'b': 2}, {}, {}], link = [-1, 0, 0, 0], length = [0, 1, 2, 3], last = 2, ch = 'c', cur = 3, p = 2`                                            |
| `nxt[p][ch] = cur`    | `nxt = [{'a': 1, 'b': 2, 'c': 3, 'd': 4}, {'b': 2}, {'c': 3}, {'..., link = [-1, 0, 0, 0, 0], length = [0, 1, 2, 3, 4], last = 3, ch = 'd', cur = 4, p = 0`              |
| `link.append(0)`      | `nxt = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'x': 5}, {'b': 2}, {'c'..., link = [-1, 0, 0, 0, 0, 0, 0], length = [0, 1, 2, 3, 4, 5, 6], last = 5, ch = 'y', cur = 6, p = -1` |
| `last = cur`          | `nxt = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'x': 5, 'y': 6, 'z': 7}..., link = [-1, 0, 0, 0, 0, 0, 0, 0], length = [0, 1, 2, 3, 4, 5, 6, 7], last = 7, ch = 'z', cur = 7`   |
| `state = link[state]` | `ch = 'a', best = 3, match = 3, state = 0`                                                                                                                               |
| `return`              | `returned = 4`                                                                                                                                                           |

### Complexity

- Time: O(n + m). A suffix automaton of the first string is built in linear time, and the second string walks through it once, keeping the length of the current match.
- Space: O(n). The automaton has at most `2n` states.
