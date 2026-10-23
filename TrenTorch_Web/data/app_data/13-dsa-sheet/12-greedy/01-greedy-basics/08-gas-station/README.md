---
name: sheet-gas-station
title: 'Gas Station'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
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

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Two facts make the answer easy:

1. If the **total gas is less than the total cost**, no start works.
2. Drive from station 0, keeping a `tank`. If it drops **below zero** at station `i`, then no station from the current start up to `i` can be a start (each one reaches `i` with at least as little fuel as the one before it... and all those trips failed). So **restart at `i + 1`** with an empty tank.

After one pass, if the total is not negative, the last restart point is the answer. It is also the smallest valid start, because every earlier start was ruled out. `O(n)`.

## Explanation

`total` checks fact 1; `tank` and `start` carry out fact 2. When the tank goes negative at `i`, the start moves to `i + 1`.
