---
name: sheet-snapshot-array
title: 'Snapshot Array'
tags: [dsa-sheet, design, classic-designs]
difficulty: Advanced
theory: snapshots-without-copying
---

## Statement

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

An array of `length` zeros supports: `"set i v"` (no result), `"snap"` (take a snapshot of the whole array; the result is the **snapshot id**, starting at 0 and increasing) and `"get i id"` (the value at position `i` **at the time of snapshot `id`**). Return the results of all `snap` and `get` operations, in order. Every `get` asks for a snapshot that exists.

For `length = 3` and `["set 0 5", "snap", "set 0 6", "get 0 0", "snap", "get 0 1"]` the answer is `[0, 5, 1, 6]`.

The starter code reads all the changes made so far for each `get`. It is correct but too slow when there are many changes.

### Examples

**Example 1**

Input:

```python
run_snapshot_array(3, ['set 0 5', 'snap', 'set 0 6', 'get 0 0', 'snap', 'get 0 1'])
```

Output:

```text
[0, 5, 1, 6]
```

**Example 2**

Input:

```python
run_snapshot_array(1, ['snap', 'get 0 0'])
```

Output:

```text
[0, 0]
```

### Constraints

- `1 <= length <= 100000`
- `0 <= len(ops) <= 100000`
- `0 <= value <= 10**9`

## Explanation

`history[i]` holds the ids and values for position `i`. `bisect_right(ids, id) - 1` is the latest entry not after the snapshot.

### Complexity

- Time: O(n log n). A `set` is O(1); a `get` is one binary search over the snapshot ids that changed that index.
- Space: O(n). One entry per change.
