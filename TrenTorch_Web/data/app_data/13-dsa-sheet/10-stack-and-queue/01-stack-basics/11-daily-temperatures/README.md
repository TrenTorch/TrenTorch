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

**Explanation:** Day 0 73 waits 1 day for 74, day 1 74 waits 1 day for 75, day 2 75 waits 4 days for 76, and later days match their next warmer distance or 0.

**Example 2**

Input:

```python
daily_temperatures([30, 40, 50, 60])
```

Output:

```text
[1, 1, 1, 0]
```

**Explanation:** Each of the first three temperatures is followed one day later by a warmer temperature, so the waits are 1,1,1 and the last day has no warmer day so 0.

### Constraints

- `0 <= len(temps) <= 200000`
- `30 <= temps[i] <= 100`

## Theory

This is "next greater element" asking for the **distance** instead of the value. Use the same **monotonic stack of indices**: keep the days that are still waiting for a warmer day. A new day `i` answers every waiting day with a lower temperature: pop each one `j` and set `out[j] = i - j`.

Storing **indices** (not temperatures) is what lets you compute the distance. `O(n)` time.

## Explanation

The stack holds days without an answer, whose temperatures do not increase from bottom to top. A warmer day pops the colder ones and tells each how long it waited.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                 | Variables                                                          |
| ------------------------------- | ------------------------------------------------------------------ |
| `out = [0] * len(temps)`        | `out = [0, 0, 0, 0, 0, 0, 0, 0]`                                   |
| `for i, t in enumerate(temps):` | `stack = [0], i = 1, t = 74`                                       |
| `j = stack.pop()`               | `out = [1, 0, 0, 0, 0, 0, 0, 0], stack = [], i = 2, t = 75, j = 1` |
| `stack.append(i)`               | `out = [1, 1, 0, 0, 0, 0, 0, 0], stack = [2, 3], i = 3, t = 71`    |
| `j = stack.pop()`               | `i = 5, t = 72, j = 4`                                             |
| `stack.append(i)`               | `out = [1, 1, 0, 2, 1, 0, 0, 0], stack = [2, 5], j = 3`            |
| `out[j] = i - j`                | `out = [1, 1, 4, 2, 1, 1, 0, 0], stack = [], i = 6, t = 76, j = 2` |
| `return`                        | `returned = [1, 1, 4, 2, 1, 1, 0, 0]`                              |

### Complexity

- Time: O(n) where n is length of temps.
- Extra space: O(n) extra for stack.
- The brute force takes O(n^2) where n is length of temps.
