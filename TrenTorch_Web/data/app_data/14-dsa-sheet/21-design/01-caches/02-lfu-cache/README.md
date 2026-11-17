---
name: sheet-lfu-cache
title: 'LFU Cache'
tags: [dsa-sheet, design, caches]
difficulty: Mastery
theory: one-bucket-per-count
---

## Statement

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

Build a **least frequently used (LFU) cache**. Operations: `"put k v"` and `"get k"` as in the LRU question; every `get` of a stored key and every `put` counts as a **use** of the key. When a `put` of a **new** key finds the cache full, remove the key with the **fewest uses**; if several have the same count, remove the **least recently used** of them. A new key starts with 1 use. A capacity of 0 stores nothing. Return the results of all `get` operations (`-1` for a missing key).

For `capacity = 2` and `["put 1 1", "put 2 2", "get 1", "put 3 3", "get 2", "get 3", "put 4 4", "get 1", "get 3", "get 4"]` the answer is `[1, -1, 3, -1, 3, 4]`.

### Examples

**Example 1**

Input:

```python
run_lfu(2, ['put 1 1', 'put 2 2', 'get 1', 'put 3 3', 'get 2', 'get 3', 'put 4 4', 'get 1', 'get 3', 'get 4'])
```

Output:

```text
[1, -1, 3, -1, 3, 4]
```

**Example 2**

Input:

```python
run_lfu(1, ['put 1 1', 'put 2 2', 'get 1', 'get 2'])
```

Output:

```text
[-1, 2]
```

### Constraints

- `0 <= capacity <= 50000`
- `0 <= len(ops) <= 100000`
- `0 <= key, value <= 10**9`

## Explanation

`count` and `value` store each key's data; `groups[c]` holds the keys with count `c` in recency order. `touch` moves a key up one group.

### Complexity

- Time: O(n). Each key sits in the ordered group of its use count, so touching or evicting a key is O(1), with `n` operations.
- Space: O(capacity). The values, the counts and the groups.
