---
name: sheet-daily-temperatures
title: 'Daily Temperatures'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
---

## Statement

`temps[i]` is the temperature on day `i`. For each day, return **how many days you must wait until a warmer day**; return `0` if there is no warmer day later.

For `[73, 74, 75, 71, 69, 72, 76, 73]` the answer is `[1, 1, 4, 2, 1, 1, 0, 0]`.

The starter code looks ahead from every day. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])
```

Output:

```text
[1, 1, 4, 2, 1, 1, 0, 0]
```

**Example 2**

Input:

```python
daily_temperatures([30, 40, 50, 60])
```

Output:

```text
[1, 1, 1, 0]
```

### Constraints

- `0 <= len(temps) <= 200000`
- `30 <= temps[i] <= 100`

## Theory

This is "next greater element" asking for the **distance** instead of the value. Use the same **monotonic stack of indices**: keep the days that are still waiting for a warmer day. A new day `i` answers every waiting day with a lower temperature: pop each one `j` and set `out[j] = i - j`.

Storing **indices** (not temperatures) is what lets you compute the distance. `O(n)` time.

## Explanation

The stack holds days without an answer, whose temperatures do not increase from bottom to top. A warmer day pops the colder ones and tells each how long it waited.
