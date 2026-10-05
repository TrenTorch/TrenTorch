---
name: data-science-pandas-missing-values
title: Missing Values: Measure, Fill, Drop
tags: [data-science, pandas, missing-data, imputation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Real tables have holes: a sensor that dropped a reading, a form field left blank, a join that found no partner. pandas marks a hole with `NaN` (or `None`, or `NaT` for dates), and what you do about it is a modelling decision with consequences. Dropping rows throws information away, and can bias the sample if the holes are not random. Filling with the overall average hides real differences between groups. Filling a time series with the last known value is reasonable for a stock price and nonsense for a count of events.

Before choosing, **measure**: how many holes, in which columns? This question builds the measuring tool, three fill strategies with different assumptions, and the habit that makes imputation honest: remembering which values were filled.

### From theory to code

Implement `missing_report(df)`, `fill_group_median(df, key, column)`, `forward_fill_limit(s, limit)`, `drop_sparse_columns(df, max_missing_fraction)` and `fill_with_indicator(df, column)`. The signatures and docstrings are already in the editor.

### Constraints

- `missing_report(df)` returns a frame indexed by column name containing **only columns with at least one missing value**, with the columns `n_missing` (integer count) and `pct` (`100 * n_missing / len(df)` rounded to 1 decimal). Rows are ordered by `n_missing` descending, ties by column name ascending. If nothing is missing it returns an empty frame with those two columns.
- `fill_group_median(df, key, column)` returns a float Series (index of `df`) equal to `df[column]` with each missing value replaced by the **median of the known values of its own group** (rows sharing the same `key`). If the group has no known value, or the row's `key` is missing, use the median of the whole column.
- `forward_fill_limit(s, limit)` carries the last known value forward into missing positions, but fills at most `limit` consecutive positions after each known value; later gaps stay missing. Leading missing values stay missing.
- `drop_sparse_columns(df, max_missing_fraction)` returns `df` without the columns whose fraction of missing values is **greater than** `max_missing_fraction` (equal is kept). Column order is kept.
- `fill_with_indicator(df, column)` returns a **copy** in which `column`'s missing values are replaced by the column median and a new boolean column `<column>_was_missing` (placed last) records which rows were filled. The input is not changed.

### Hints

<details>
<summary>Hint 1</summary>

`df.isna().sum()` counts the holes per column; `.mean()` instead of `.sum()` gives the fraction.

</details>

<details>
<summary>Hint 2</summary>

`groupby(key)[column].transform("median")` writes each group's median onto every row. Fill from it first, then from the overall median for what is left.

</details>

<details>
<summary>Hint 3</summary>

`Series.ffill` has a `limit` argument.

</details>

## Theory

### The simple version

A survey comes back with some questions unanswered. You can throw away every incomplete form (and maybe lose most of them), guess a typical answer for the blanks, copy the previous person's answer, or leave the blank and say so. Each choice is defensible somewhere and wrong somewhere else, which is why the first step is counting the blanks.

### Measuring

`df.isna()` is a boolean frame the shape of `df`. Summing it counts holes per column, averaging gives the fraction:

$$
\text{missing fraction}_j = \frac{1}{n}\sum_{i=1}^{n}\mathbf{1}[x_{ij}\ \text{is missing}]
$$

A column that is 60% empty is usually dropped; one that is 2% empty is usually filled. The threshold is a judgement call, which is why it is a parameter.

### Why missingness matters

Statisticians distinguish three cases. _Missing completely at random_ (a dropped packet) is harmless to ignore. _Missing at random given other columns_ (older customers skip an income question) can be handled by using those columns, which is what a group median does. _Missing not at random_ (people with high debt skip the debt question) cannot be repaired by any fill; the hole itself carries information.

### Strategies

| Strategy              | Assumes                          | Risk                                     |
| --------------------- | -------------------------------- | ---------------------------------------- |
| drop rows / columns   | holes are rare or random         | loses data, can bias                     |
| global mean or median | one typical value                | flattens group differences               |
| **group** median      | holes are explained by the group | tiny groups give noisy fills             |
| forward fill          | value persists over time         | stale values over long gaps (so `limit`) |
| fill + indicator      | the hole is itself informative   | one more column                          |

The median is preferred over the mean for filling because a few extreme values barely move it.

### Keep a record

After filling, "this value was observed" and "this value was invented" look identical. An indicator column keeps them apart so a model can learn from missingness, and so an analyst can check how much of a result depends on filled values.

### How pandas actually implements this

Missing is stored per dtype: `NaN` for floats, a mask for the nullable dtypes, `NaT` for datetimes. `isna` is a vectorised check against that representation. `fillna(Series)` aligns on the index before filling; `ffill` walks the array once keeping the last valid position, and `limit` stops it counting after that many steps.

## Explanation

`missing_report` counts holes with `isna().sum()`, keeps columns with at least one, rounds the percentage to one decimal and orders by count descending then name. `fill_group_median` fills first from each group's median (computed with `transform`, which ignores missing values) and then from the column's overall median, which covers groups with no known value and rows with no key. `forward_fill_limit` is `ffill(limit=...)`. `drop_sparse_columns` keeps columns whose missing fraction is at most the threshold. `fill_with_indicator` records `isna()` before filling, so the indicator reflects the original data.
