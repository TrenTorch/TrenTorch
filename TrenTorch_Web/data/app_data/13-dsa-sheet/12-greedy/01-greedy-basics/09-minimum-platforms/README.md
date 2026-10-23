---
name: sheet-minimum-platforms
title: 'Minimum Platforms'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
---

## Statement

Train `i` arrives at time `arrivals[i]` and leaves at `departures[i]` (`arrivals[i] <= departures[i]`). It occupies a platform for the whole time from arrival to departure, **both ends included**: a train arriving at the same time another one leaves needs a different platform. Return the **fewest platforms** needed so that no train has to wait.

For `arrivals = [900, 940, 950, 1100, 1500, 1800]` and `departures = [910, 1200, 1120, 1130, 1900, 2000]` the answer is `3`.

The starter code counts the trains in the station for every arrival. It is correct but too slow for many trains.

### Examples

**Example 1**

Input:

```python
min_platforms([900, 940, 950, 1100, 1500, 1800], [910, 1200, 1120, 1130, 1900, 2000])
```

Output:

```text
3
```

**Example 2**

Input:

```python
min_platforms([900, 1100, 1235], [1000, 1200, 1240])
```

Output:

```text
1
```

### Constraints

- `0 <= number of trains <= 200000`
- `0 <= arrivals[i] <= departures[i] <= 10**9`

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

The number of platforms needed is the **largest number of trains in the station at the same moment**. That number only changes at arrival and departure times, so you can sweep through time.

Sort the arrival times and the departure times **separately**. Walk through both with two pointers: if the next event is an arrival (arrival time `<=` next departure time, since equal times count as overlap), a train comes in: `current += 1` and update the maximum; otherwise a train leaves: `current -= 1`.

You never need to know which train leaves, only how many are present. `O(n log n)`.

## Explanation

At equal times the arrival is processed before the departure, which gives the inclusive overlap the statement asks for.
