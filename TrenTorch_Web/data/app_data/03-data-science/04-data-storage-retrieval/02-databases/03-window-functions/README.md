---
name: data-storage-window-functions
title: Window Functions
tags: [databases, window-functions]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-group-by` collapses each group to a single row. Many questions need the opposite: keep every row and attach a number computed from its neighbours. The running total of an account balance, the rank of each salary within a department, the change from the previous day, a seven-day moving average. These are **window functions**. Each row looks at a window of related rows (its own partition, up to the current position) and computes a value without removing any row. They are among the most useful and most misread tools in SQL, and the same logic builds time-series features for models. This question builds the four most common ones over rows that are already in order.

### From theory to code

Implement `running_sum(values, partitions)`, a cumulative total that restarts in each partition, then `rank(values, partitions)`, the standard competition ranking within each partition, then `lag(values, partitions, offset, default)`, the value from an earlier row in the same partition, then `moving_average(values, window)`, the average of the last few values. The signatures and docstrings are already in the editor.

### Constraints

- `values` and `partitions` are lists of the same length, in the **row order** of the table (the order the window follows). `partitions[i]` is the partition label of row `i`. Rows of one partition may be interleaved with others, and within a partition the order is the row order.
- `running_sum(values, partitions)` returns a list where entry `i` is the sum of `values[j]` over rows `j <= i` in the same partition as row `i`.
- `rank(values, partitions)` returns a list of ranks where entry `i` is `1 + (number of rows in the same partition with a strictly larger value)`: the highest value has rank 1, **ties share a rank and the next rank is skipped** (values 9, 9, 7 have ranks 1, 1, 3).
- `lag(values, partitions, offset, default)` returns a list where entry `i` is the value of the row `offset` rows earlier **within the same partition**, or `default` if there is no such row. `offset >= 1`.
- `moving_average(values, window)` ignores partitions and returns a list of floats where entry `i` is the mean of `values[max(0, i - window + 1) : i + 1]`, so early entries average over fewer values. `window >= 1`.
- Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

Keep one running state per partition in a dict, updated as you walk the rows in order. A row only ever needs the state of its own partition.

</details>

<details>
<summary>Hint 2</summary>

For `lag`, keep the list of values seen so far in each partition. The value `offset` rows back is at position `len(seen) - offset`, if that position exists.

</details>

<details>
<summary>Hint 3</summary>

Rank counts how many values in the partition beat this one, which is why equal values get the same rank and leave a gap after them.

</details>

## Theory

### The simple version

A running total on a bank statement is the cleanest picture: every line still shows its own transaction, with the balance so far added at the end. Nothing was collapsed, each row just got a column computed from the rows above it. If the statement covered several accounts, each account would have its own running balance, restarting where it begins. The account is the partition and the order of the lines is the window.

### The formula

Number the rows $0, \dots, n-1$ in order and let $P(i)$ be the set of rows $j \le i$ in the same partition as row $i$. Then

$$
\text{running\_sum}_i = \sum_{j \in P(i)} v_j, \qquad \text{lag}_i^{(k)} = v_{j}\ \text{where } j \text{ is the } k\text{-th row before } i \text{ in } P(i)
$$

**Rank** within a partition $Q$ is

$$
\text{rank}_i = 1 + \big|\{\, j \in Q : v_j > v_i \,\}\big|
$$

so equal values share a rank and the following rank is skipped (SQL's `RANK`). `DENSE_RANK` would not skip, and `ROW_NUMBER` would break ties arbitrarily.

A **moving average** over a trailing window of width $w$ is

$$
\text{ma}_i = \frac{1}{\min(w,\, i + 1)} \sum_{j = \max(0,\, i - w + 1)}^{i} v_j
$$

- The window is defined by row order, so the order must be stated: a running total is meaningless on an unordered table.
- `PARTITION BY` splits the table into independent windows, and `ORDER BY` inside `OVER` sets the row order within each.
- A running sum and a moving average can be updated in constant time per row by adding the new value and subtracting the one that left the window.

### Window functions versus group-by

A group-by returns one row per group. A window function returns every input row, so the results can be added as a new column of the original table. The two combine freely: aggregate with a group-by, then join the totals back, or compute the same result directly with a window.

### In feature engineering

Lag features (yesterday's value), rolling means and running counts are the standard inputs for forecasting and for per-user behaviour models. They must only look backwards: a window that includes future rows hands the model the answer, the time-series version of leakage.

### How NumPy/PyTorch actually implements this

SQL's `SUM(x) OVER (PARTITION BY p ORDER BY t)`, `RANK()`, `LAG(x, k)` and `AVG(x) OVER (ROWS BETWEEN w-1 PRECEDING AND CURRENT ROW)` are these four. In pandas, `groupby(p)[x].cumsum()`, `groupby(p)[x].rank(method='min', ascending=False)`, `groupby(p)[x].shift(k)` and `x.rolling(w, min_periods=1).mean()` compute them. `np.cumsum` and `np.convolve` do the unpartitioned versions, and `torch.cumsum` and `torch.nn.functional.avg_pool1d` do them on tensors.

## Explanation

`running_sum` walks the rows once keeping a dict of running totals per partition, adding each value to its partition's total and recording the new total. `rank` counts, for each row, how many values in the same partition are strictly larger and adds one, which gives ties the same rank and skips the following ones. `lag` keeps, per partition, the list of values seen so far, and for each row looks `offset` places back in that list, falling back to `default` when the partition does not have enough earlier rows. `moving_average` slices the window ending at each position and averages it, shorter at the start. Each function reads its inputs without changing them.
