---
name: sheet-time-based-key-value-store
title: 'Time-Based Key-Value Store'
tags: [dsa-sheet, design, classic-designs]
difficulty: Intermediate
theory: a-store-with-timestamps
---

## Statement

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

Build a store where every value has a **timestamp**. Operations: `"set key value t"` stores `value` for `key` at time `t` (the times of the `set` operations only increase); `"get key t"` returns the value stored for `key` at the **latest time that is at most `t`**, or an empty string if there is none. Return the results of all `get` operations.

For `["set love high 10", "get love 10", "get love 15", "set love low 20", "get love 15", "get love 25", "get love 5"]` the answer is `["high", "high", "high", "low", ""]`.

The starter code scans every value of the key for each `get`. It is correct but too slow when a key has many values.

### Examples

**Example 1**

Input:

```python
run_time_map(['set love high 10', 'get love 10', 'get love 15', 'set love low 20', 'get love 15', 'get love 25', 'get love 5'])
```

Output:

```text
['high', 'high', 'high', 'low', '']
```

**Example 2**

Input:

```python
run_time_map(['get a 1'])
```

Output:

```text
['']
```

### Constraints

- `0 <= len(ops) <= 100000`
- Keys and values are lower-case words or numbers without spaces.
- The times of the `set` operations strictly increase.

## Explanation

`times[key]` and `values[key]` are parallel lists. `bisect_right(times, t)` is the number of entries with time `<= t`, so the entry before that index is the answer.

### Complexity

- Time: O(n log n). A `set` appends in O(1) because times grow; a `get` is one binary search over the times of that key.
- Space: O(n). All stored values.
