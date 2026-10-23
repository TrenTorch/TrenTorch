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

**Example 2**

Input:

```python
run_hit_counter(['count 5'])
```

Output:

```text
[0]
```

### Constraints

- `0 <= len(ops) <= 100000`
- `1 <= t <= 10**9`; the seconds are not decreasing.

## Theory

In a **design** question you build a small data structure and run a list of operations on it. The operations are given as text, one per string, and you return the answers of the operations that produce one. Think about which operations must be fast and choose the data structure for them.

Hits arrive in time order, so the oldest are at the front. Keep the hits in a **queue** (`collections.deque`). Before answering a `count t`, **remove from the front** every hit that is older than the window (`hit <= t - 300`). What is left in the queue is exactly the answer, `len(queue)`.

Each hit enters the queue once and leaves once, so all operations are `O(1)` amortised. (If many hits share the same second, you can store `(second, count)` pairs instead.)

## Explanation

`window` holds the hits that may still count. The `while` loop discards the expired ones before measuring its length.
