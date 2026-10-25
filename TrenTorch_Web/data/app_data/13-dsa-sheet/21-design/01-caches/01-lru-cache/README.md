---
name: sheet-lru-cache
title: 'LRU Cache'
tags: [dsa-sheet, design, caches]
difficulty: Intermediate
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

**Explanation:** Size 2 cache holds 1 and 2. get 1 recent. put 3 evicts 2. get 2 is -1. put 4 evicts 1. get 1 is -1, get 3 gives 3, get 4 gives 4.

**Example 2**

Input:

```python
run_lru(0, ['put 1 1', 'get 1'])
```

Output:

```text
[-1]
```

**Explanation:** Capacity zero means the cache never stores entries. put 1 1 is ignored. get 1 finds nothing, so returns -1.

### Constraints

- `0 <= capacity <= 100000`
- `0 <= len(ops) <= 100000`
- `0 <= key, value <= 10**9`

## Theory

The cache must find a key in `O(1)` **and** know which key was used least recently, moving a key to the "most recent" end in `O(1)`. A dictionary alone has no order of use; a list has the order but needs `O(n)` to find or remove a key.

Combine them: a **hash map plus a doubly linked list** (the classic answer), or in Python an **`OrderedDict`**, which is exactly that. `move_to_end(key)` marks a key as most recent, and `popitem(last=False)` removes the oldest. All operations are `O(1)`.

## Explanation

`cache` keeps keys in the order of use, oldest first. Reading or writing a key moves it to the end; a new key beyond the capacity evicts the first one.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables                                                                                                  |
| --------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `cache = OrderedDict()`     | `cache = OrderedDict()`                                                                                    |
| `for op in ops:`            | `cache = OrderedDict([(1, 1)]), out = [], op = 'put 2 2', parts = ['put', '1', '1'], key = 1, value = 1`   |
| `key = int(parts[1])`       | `cache = OrderedDict([(1, 1), (2, 2)]), op = 'get 1', parts = ['get', '1'], value = 2`                     |
| `cache.popitem(last=False)` | `cache = OrderedDict([(1, 1)]), out = [1], op = 'put 3 3', parts = ['put', '3', '3'], key = 3, value = 3`  |
| `parts = op.split()`        | `cache = OrderedDict([(1, 1), (3, 3)]), out = [1, -1], op = 'put 4 4', parts = ['put', '4', '4'], key = 2` |
| `key = int(parts[1])`       | `cache = OrderedDict([(3, 3), (4, 4)]), op = 'get 1', parts = ['get', '1'], key = 1, value = 4`            |
| `out.append(cache[key])`    | `cache = OrderedDict([(4, 4), (3, 3)]), out = [1, -1, -1, 3], op = 'get 3', parts = ['get', '3'], key = 3` |
| `return`                    | `returned = [1, -1, -1, 3, 4]`                                                                             |

### Complexity

- Time: O(n) where n is number of operations.
- Extra space: O(q) q = cache capacity.
- The brute force takes O(n^2) n = ops count.
