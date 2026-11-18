---
name: sheet-minimum-platforms
title: 'Minimum Platforms'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Intermediate
theory: counting-overlaps-platforms
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

## Explanation

At equal times the arrival is processed before the departure, which gives the inclusive overlap the statement asks for.

### Complexity

- Time: O(n log n). Sorting arrivals and departures dominates; the sweep is O(n).
- Space: O(n). The two sorted copies.
