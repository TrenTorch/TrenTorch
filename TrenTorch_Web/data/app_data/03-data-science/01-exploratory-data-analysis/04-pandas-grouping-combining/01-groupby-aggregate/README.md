---
name: data-science-pandas-groupby-aggregate
title: GroupBy & Aggregation
tags: [data-science, pandas, groupby, aggregation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Almost every real question about a table is a question about _groups_: average salary **per department**, orders **per customer**, the best-selling product **per month**. The idea behind all of them is the same three steps, usually called split-apply-combine. Split the rows into groups by a key. Apply something to each group. Combine the results back into one table.

What you _apply_ decides the shape of the answer, and that is the part that trips people. Aggregating (a mean) collapses each group to one row. Transforming (the group's mean written next to every member) keeps every row. Selecting (the top two per group) keeps some rows. This question builds one of each, and a fourth, a within-group z-score, that needs a transform with a spread.

### From theory to code

Implement `group_summary(df, key, value)`, `add_group_mean(df, key, value)`, `zscore_within_group(df, key, value)` and `top_n_per_group(df, key, value, n)`. The signatures and docstrings are already in the editor.

### Constraints

- Rows whose `key` is missing belong to no group: they are left out of every group statistic.
- `group_summary(df, key, value)` returns a frame **indexed by the distinct keys, sorted ascending**, with the columns `n` (count of non-missing `value`s, integer), `mean`, `median` and `max` of `value`, in that order. A group whose values are all missing still appears, with `n = 0` and `NaN` statistics.
- `add_group_mean(df, key, value)` returns a **copy** of `df` with one new column, `<value>_group_mean`, holding the mean of `value` over the row's group (missing values ignored). Rows with a missing key get `NaN`. The original frame is not changed.
- `zscore_within_group(df, key, value)` returns a float Series with `df`'s index: `(value - group mean) / group std`, with the **sample** standard deviation (divide by `n - 1`). It is `NaN` where the value is missing, the group has one value, the standard deviation is `0`, or the key is missing.
- `top_n_per_group(df, key, value, n)` returns, for each key, the `n` rows with the largest `value` (ties keep their original order; rows with a missing key or value are ignored). The result has all of `df`'s columns and original index labels, ordered by key ascending, then by `value` descending within a key.

### Hints

<details>
<summary>Hint 1</summary>

`groupby(key)[value].agg(...)` accepts named aggregations such as `n="count"`.

</details>

<details>
<summary>Hint 2</summary>

`transform` returns a result the same length as the input, aligned to the original rows. That is what lets a group statistic sit next to each member.

</details>

<details>
<summary>Hint 3</summary>

For the top rows of each group, sort by `value` descending first, then take the first `n` of every group with `groupby(...).head(n)`.

</details>

## Theory

### The simple version

Sort a class's exam papers into piles by teacher (split). Work out each pile's average (apply). Write the averages on a single sheet, one line per teacher (combine). If instead you wanted to write each pile's average on _every paper_ in the pile, that is a different "combine": keep all the papers and attach the number. Same grouping, different result shape.

<div class="tt-widget" data-widget="data-science-pandas-groupby-aggregate"></div>

### Three shapes of "apply"

| Step            | Returns                 | Shape                  | Pandas verb                  |
| --------------- | ----------------------- | ---------------------- | ---------------------------- |
| aggregate       | one value per group     | one row per group      | `agg`, `mean`, `count`, ...  |
| transform       | one value per row       | same rows as the input | `transform`                  |
| filter / select | some rows of each group | a subset of the rows   | `head`, `nlargest`, `filter` |

### Group statistics

For a group $G$ with non-missing values $x_i$ and size $n_G$:

$$
\bar{x}_G = \frac{1}{n_G}\sum_{i\in G}x_i, \qquad
s_G = \sqrt{\frac{1}{n_G-1}\sum_{i\in G}(x_i-\bar{x}_G)^2}, \qquad
z_i = \frac{x_i-\bar{x}_G}{s_G}
$$

The z-score re-expresses each value as "how many standard deviations above its own group's mean", which makes salaries from different departments, or marks from different teachers, comparable. It is undefined when $n_G = 1$ (no spread to measure) or $s_G = 0$ (everyone equal).

### Missing keys and empty groups

By default `groupby` drops rows whose key is `NaN`. Statistics skip missing values: `count` counts only the known ones, so a group of all-missing values has `count = 0` and `NaN` for the mean, which is a more honest result than `0`.

### Top-N per group

There is no single call that means "the best two in each group". The reliable recipe is: sort the whole frame by the ranking column (stable), take the first $n$ rows of each group with `groupby(key).head(n)`, then order the output the way you want to read it.

### How pandas actually implements this

`groupby` factorises the key column into integer codes (a hash table), then computes each aggregation in compiled loops over those codes ("cython groupby"), which is why it is fast. A transform runs the same loop and then _broadcasts_ each group's result back to the original row positions. `head(n)` is a rank-within-group filter: it numbers rows inside each group and keeps those with number below $n$.

## Explanation

`group_summary` uses a named aggregation (`count`, `mean`, `median`, `max`) and sorts by key, so a group of only missing values still appears with `n = 0`. `add_group_mean` adds a column computed with `transform("mean")`, which is aligned to the original rows. `zscore_within_group` subtracts the group mean and divides by the group's sample standard deviation, both obtained with `transform`, and masks the places where the spread is not positive. `top_n_per_group` drops rows without a key or a value, sorts by the value descending with a stable sort, keeps `head(n)` of every group, and stable-sorts by key so the value order is preserved inside each key.
