---
name: sheet-lfu-cache
title: 'LFU Cache'
tags: [dsa-sheet, design, caches]
difficulty: Mastery
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

**Explanation:** After inserting keys 1 and 2, key 1 is accessed, raising its count; inserting key 3 removes key 2, the least frequently used; subsequent inserts and accesses produce results [1,-1,3,-1,3,4].

**Example 2**

Input:

```python
run_lfu(1, ['put 1 1', 'put 2 2', 'get 1', 'get 2'])
```

Output:

```text
[-1, 2]
```

**Explanation:** With capacity 1, first put stores key 1; second put evicts it; 'get 1' returns -1; 'get 2' returns 2.

### Constraints

- `0 <= capacity <= 50000`
- `0 <= len(ops) <= 100000`
- `0 <= key, value <= 10**9`

## Theory

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

Two orders matter: the **use count** and, inside one count, the **recency**. Group the keys by their count: `groups[c]` is an `OrderedDict` of the keys used exactly `c` times, oldest first. Keep `min_count`, the smallest count that exists.

- A use of key `k` with count `c`: remove it from `groups[c]`, add it to the end of `groups[c + 1]`; if `groups[c]` became empty and `c == min_count`, `min_count += 1`.
- Evicting: pop the oldest key of `groups[min_count]`.
- A new key goes into `groups[1]` and `min_count = 1`.

Every operation is `O(1)`.

## Explanation

`count` and `value` store each key's data; `groups[c]` holds the keys with count `c` in recency order. `touch` moves a key up one group.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line     | Variables                                                                                                                                                                                     |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `value = {}`        | `value = {}`                                                                                                                                                                                  |
| `count[key] = 1`    | `value = {1: 1}, count = {1: 1}, groups = {}, low = 0, touch = <function run_lfu.<locals>.touch at 0x000001F482DF64D0>, out = [], op = 'put 1 1', parts = ['put', '1', '1'], key = 1`         |
| `for op in ops:`    | `value = {1: 1, 2: 2}, count = {1: 1, 2: 1}, groups = {1: OrderedDict([(1, None), (2, None)])}, low = 1, op = 'get 1', parts = ['put', '2', '2'], key = 2`                                    |
| `del value[oldest]` | `value = {1: 1}, count = {1: 2, 2: 1}, groups = {2: OrderedDict([(1, None)])}, out = [1], op = 'put 3 3', parts = ['put', '3', '3'], key = 3, oldest = 2, _ = None`                           |
| `for op in ops:`    | `value = {1: 1, 3: 3}, count = {1: 2, 3: 1}, groups = {2: OrderedDict([(1, None)]), 1: OrderedDict([(3, None)])}, out = [1, -1], op = 'get 3', parts = ['get', '2'], key = 2`                 |
| `del count[oldest]` | `value = {3: 3}, count = {3: 2}, groups = {2: OrderedDict([(3, None)])}, low = 2, out = [1, -1, 3], op = 'put 4 4', parts = ['put', '4', '4'], key = 4, oldest = 1`                           |
| `for op in ops:`    | `value = {3: 3, 4: 4}, count = {3: 2, 4: 1}, groups = {2: OrderedDict([(3, None)]), 1: OrderedDict([(4, None)])}, low = 1, out = [1, -1, 3, -1], op = 'get 3', parts = ['get', '1'], key = 1` |
| `return`            | `returned = [1, -1, 3, -1, 3, 4]`                                                                                                                                                             |
