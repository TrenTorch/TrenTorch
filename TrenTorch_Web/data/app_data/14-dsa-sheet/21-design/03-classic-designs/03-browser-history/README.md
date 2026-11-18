---
name: sheet-browser-history
title: 'Browser History'
tags: [dsa-sheet, design, classic-designs]
difficulty: Intermediate
theory: a-list-and-a-pointer
---

## Statement

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

A browser starts on `homepage`. Operations: `"visit url"` goes to a new page (all pages ahead in the history are forgotten); `"back k"` goes back up to `k` pages (as far as the first page); `"forward k"` goes forward up to `k` pages (as far as the last page). Return the **current page after each `back` and each `forward`**, in order. `visit` has no result.

For `homepage = "a"` and `["visit b", "visit c", "back 1", "back 5", "forward 1", "visit d", "forward 3"]` the answer is `["b", "a", "b", "d"]`.

### Examples

**Example 1**

Input:

```python
run_browser_history('a', ['visit b', 'visit c', 'back 1', 'back 5', 'forward 1', 'visit d', 'forward 3'])
```

Output:

```text
['b', 'a', 'b', 'd']
```

**Example 2**

Input:

```python
run_browser_history('a', ['back 1'])
```

Output:

```text
['a']
```

### Constraints

- `0 <= len(ops) <= 100000`
- Pages are words without spaces; `1 <= k <= 100`.

## Explanation

The list is the whole history and `index` points into it. `del history[index + 1 :]` forgets the forward pages on a visit.

### Complexity

- Time: O(n). Every operation is O(1), except that a `visit` drops the forward pages, each page being dropped at most once.
- Space: O(n). The list of pages.
