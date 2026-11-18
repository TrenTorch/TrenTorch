---
name: sheet-gas-station
title: 'Gas Station'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
theory: gas-station
---

## Statement

There are `n` gas stations on a circular road. Station `i` gives `gas[i]` units of fuel and driving from station `i` to the next station costs `cost[i]`. Your tank is empty and unlimited in size. Return the **smallest index** of a station where you can start and drive once around the circle, or `-1` if it cannot be done.

For `gas = [1, 2, 3, 4, 5]` and `cost = [3, 4, 5, 1, 2]` the answer is `3`.

The starter code simulates a trip from every station. It is correct but too slow for many stations.

### Examples

**Example 1**

Input:

```python
gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
```

Output:

```text
3
```

**Example 2**

Input:

```python
gas_station([2, 3, 4], [3, 4, 3])
```

Output:

```text
-1
```

### Constraints

- `0 <= n <= 200000`
- `0 <= gas[i], cost[i] <= 10**4`

## Explanation

`total` checks fact 1; `tank` and `start` carry out fact 2. When the tank goes negative at `i`, the start moves to `i + 1`.

### Complexity

- Time: O(n). One pass; if the tank goes negative no station up to here can be the start, so the next one is tried.
- Space: O(1). A few numbers.
