---
name: sheet-time-based-key-value-store
title: 'Time-Based Key-Value Store'
tags: [dsa-sheet, design, classic-designs]
difficulty: Intermediate
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

**Explanation:** The first set stores high at time 10, so get at 10 and 15 retrieve that value; the second set at 20 stores low, which is returned for get at 25; get at 5 returns empty because no entry <=5.

**Example 2**

Input:

```python
run_time_map(['get a 1'])
```

Output:

```text
['']
```

**Explanation:** No 'set' operations for key a, so the single get at time 1 yields an empty string.

### Constraints

- `0 <= len(ops) <= 100000`
- Keys and values are lower-case words or numbers without spaces.
- The times of the `set` operations strictly increase.

## Theory

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

For each key keep the list of its `(time, value)` pairs. Because the times only increase, each list is **already sorted by time**. A `get` asks for the last pair with time `<= t`: a **binary search** (`bisect_right` on the list of times, minus one).

`set` is `O(1)` (append) and `get` is `O(log m)` for a key with `m` values.

## Explanation

`times[key]` and `values[key]` are parallel lists. `bisect_right(times, t)` is the number of entries with time `<= t`, so the entry before that index is the answer.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                        | Variables                                                                                                               |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `times = {}`                                           | `times = {}`                                                                                                            |
| `parts = op.split()`                                   | `values = {}, out = [], op = 'set love high 10', parts = ['set', 'love', 'high', '10']`                                 |
| `key = parts[1]`                                       | `times = {'love': [10]}, values = {'love': ['high']}, op = 'get love 10', parts = ['get', 'love', '10'], key = 'love'`  |
| `parts = op.split()`                                   | `out = ['high'], op = 'get love 15', parts = ['get', 'love', '15'], i = 1`                                              |
| `times.setdefault(parts[1], []).append(int(parts[3]))` | `times = {'love': [10, 20]}, out = ['high', 'high'], op = 'set love low 20', parts = ['set', 'love', 'low', '20']`      |
| `out.append(values[key][i - 1] if i else "")`          | `values = {'love': ['high', 'low']}, out = ['high', 'high', 'high'], op = 'get love 15', parts = ['get', 'love', '15']` |
| `for op in ops:`                                       | `out = ['high', 'high', 'high', 'low'], op = 'get love 5', parts = ['get', 'love', '25'], i = 2`                        |
| `return`                                               | `returned = ['high', 'high', 'high', 'low', '']`                                                                        |

### Complexity

- Time: O(n log n) where n=total operations, q=get calls.
- Extra space: O(n) extra memory where n=number of set operations.
- The brute force takes O(n^2) where n=total operations.
