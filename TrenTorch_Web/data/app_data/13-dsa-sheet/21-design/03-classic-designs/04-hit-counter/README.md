---
name: sheet-hit-counter
title: 'Hit Counter'
tags: [dsa-sheet, design, classic-designs]
difficulty: Intermediate
---

## Statement

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

A web page counts hits. Operations: `"hit t"` records a hit at second `t`; `"count t"` asks for the **number of hits in the last 300 seconds**, that is, at seconds `t - 299` up to `t`. The seconds in the operations never decrease. Return the results of all `count` operations.

For `["hit 1", "hit 2", "hit 3", "count 4", "hit 300", "count 300", "count 301"]` the answer is `[3, 4, 3]`.

The starter code looks at all the hits ever recorded for each count. It is correct but too slow for a long log.

### Examples

**Example 1**

Input:

```python
run_hit_counter(['hit 1', 'hit 2', 'hit 3', 'count 4', 'hit 300', 'count 300', 'count 301'])
```

Output:

```text
[3, 4, 3]
```

**Explanation:** Hits at times 1, 2, 3 are accumulated, so count at time 4 outputs 3. The hit at 300 enters the window, giving 4 hits by time 300, and 3 hits at time 301.

**Example 2**

Input:

```python
run_hit_counter(['count 5'])
```

Output:

```text
[0]
```

**Explanation:** Only a count operation with no prior hits yields 0.

### Constraints

- `0 <= len(ops) <= 100000`
- `1 <= t <= 10**9`; the seconds are not decreasing.

## Theory

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

Hits arrive in time order, so the oldest are at the front. Keep the hits in a **queue** (`collections.deque`). Before answering a `count t`, **remove from the front** every hit that is older than the window (`hit <= t - 300`). What is left in the queue is exactly the answer, `len(queue)`.

Each hit enters the queue once and leaves once, so all operations are `O(1)` amortised. (If many hits share the same second, you can store `(second, count)` pairs instead.)

## Explanation

`window` holds the hits that may still count. The `while` loop discards the expired ones before measuring its length.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line        | Variables                                                                 |
| ---------------------- | ------------------------------------------------------------------------- |
| `window = deque()`     | `window = deque([])`                                                      |
| `t = int(t)`           | `out = [], op = 'hit 1', kind = 'hit', t = 1`                             |
| `window.append(t)`     | `window = deque([1, 2]), op = 'hit 2', t = 2`                             |
| `window.append(t)`     | `window = deque([1, 2, 3]), op = 'hit 3', t = 3`                          |
| `for op in ops:`       | `out = [3], op = 'hit 300', kind = 'count', t = 4`                        |
| `for op in ops:`       | `window = deque([1, 2, 3, 300]), op = 'count 300', kind = 'hit', t = 300` |
| `kind, t = op.split()` | `out = [3, 4], op = 'count 301', kind = 'count', t = '301'`               |
| `return`               | `returned = [3, 4, 3]`                                                    |

### Complexity

- Time: O(n + q), where n is the number of hits and q is the number of count operations. The deque efficiently tracks active hits, allowing for O(1) lookup and removal of expired hits during count operations.
- Extra space: O(n), where n is the maximum number of hits within the 300-second window. The deque stores all active hits, and its size does not exceed the window duration.
- The brute force takes O(n * q), where n is the total number of hits and q is the number of count operations. Each count operation requires scanning the entire list of hits to check if they fall within the 300-second window, leading to quadratic time complexity relative to the number of counts.
