---
name: sheet-browser-history
title: 'Browser History'
tags: [dsa-sheet, design, classic-designs]
difficulty: Intermediate
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

## Theory

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

Keep the history in a **list** and an **index** of the current page. `visit`: drop everything after the index (`del history[index + 1:]`), append the new page, move the index to it. `back k`: `index = max(0, index - k)`. `forward k`: `index = min(len(history) - 1, index + k)`. Every operation is `O(1)` amortised (the deletion of the forward pages is paid by the earlier visits).

## Explanation

The list is the whole history and `index` points into it. `del history[index + 1 :]` forgets the forward pages on a visit.
