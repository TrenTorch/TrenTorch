---
name: sheet-lru-cache
title: 'LRU Cache'
tags: [dsa-sheet, design, caches]
difficulty: Intermediate
theory: dictionary-plus-list
---

## Statement

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

Build a **least recently used (LRU) cache** with a given `capacity`. Operations: `"put k v"` stores the value `v` for the key `k`; `"get k"` returns the value of `k`, or `-1` if it is not in the cache. Both count as a **use** of the key. When a `put` of a new key finds the cache full, first remove the **least recently used** key. A capacity of 0 stores nothing. Return the results of all `get` operations, in order.

For `capacity = 2` and `["put 1 1", "put 2 2", "get 1", "put 3 3", "get 2", "put 4 4", "get 1", "get 3", "get 4"]` the answer is `[1, -1, -1, 3, 4]`.

The starter code keeps the keys in a list and searches it. It is correct but too slow for a big cache.

### Examples

**Example 1**

Input:

```python
run_lru(2, ['put 1 1', 'put 2 2', 'get 1', 'put 3 3', 'get 2', 'put 4 4', 'get 1', 'get 3', 'get 4'])
```

Output:

```text
[1, -1, -1, 3, 4]
```

**Example 2**

Input:

```python
run_lru(0, ['put 1 1', 'get 1'])
```

Output:

```text
[-1]
```

### Constraints

- `0 <= capacity <= 100000`
- `0 <= len(ops) <= 100000`
- `0 <= key, value <= 10**9`

## Explanation

`cache` keeps keys in the order of use, oldest first. Reading or writing a key moves it to the end; a new key beyond the capacity evicts the first one.

### Complexity

- Time: O(n). `OrderedDict` gets, moves and evicts in O(1) each, with `n` operations.
- Space: O(capacity). The cache.
