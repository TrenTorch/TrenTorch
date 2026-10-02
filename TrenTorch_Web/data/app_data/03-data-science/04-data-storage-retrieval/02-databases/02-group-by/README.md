---
name: data-storage-group-by
title: 'Group-By & Aggregation'
tags: [databases, aggregation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A table of ten million orders is rarely the answer to a question. Revenue per country, the average basket size per week and the number of customers per plan are. Those are **group-by** questions: split the rows into groups by one or more columns, then collapse each group into a few summary numbers with an aggregate such as a count, a sum or a mean. It is the central operation of reporting and of feature engineering, and it is a hash table in disguise, with one bucket per group. This question builds the operation with several aggregates at once and the filter that applies after grouping.

### From theory to code

Implement `group_by(rows, keys, aggregations)`, which splits rows into groups and computes the requested aggregates for each, then `having(groups, predicate)`, which keeps only groups that satisfy a condition, then `count_distinct(rows, column)`, which counts different values in a column. The signatures and docstrings are already in the editor.

### Constraints

- `rows` is a list of dicts. `keys` is a non-empty list of column names defining the group. `aggregations` is a dict mapping an output column name to a pair `(column, function_name)` where `function_name` is one of `"count"`, `"sum"`, `"mean"`, `"min"`, `"max"`. For `"count"` the column is ignored and the number of rows in the group is returned.
- `group_by` returns a list of dicts, one per distinct combination of the key columns, sorted ascending by the tuple of key values. Each output dict has the key columns, then the aggregate columns in the order of `aggregations`.
- Aggregates ignore rows whose value in the aggregated column is `None`. `"mean"` is the sum divided by the number of non-`None` values. If a group has no non-`None` values for a `sum`, `mean`, `min` or `max`, the result is `None`. `"count"` counts every row, `None` or not.
- An unknown `function_name` raises `ValueError`. An empty table returns `[]`.
- `having(groups, predicate)` returns the list of group dicts for which `predicate(group)` is true, in the original order.
- `count_distinct(rows, column)` returns the number of different non-`None` values in the column, as an int. The input must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

Go through the rows once and keep a dict from the key tuple to the list of rows in that group. A tuple is hashable, so it can be a dict key even when the group is defined by several columns.

</details>

<details>
<summary>Hint 2</summary>

Compute every aggregate from the group's list of values after dropping the `None` values, and handle the empty case once instead of in each branch.

</details>

<details>
<summary>Hint 3</summary>

`having` is the filter that sees the aggregate results. A plain filter on rows before grouping cannot say "only groups with at least five rows".

</details>

## Theory

### The simple version

Sort a pile of receipts into one stack per shop, then for each stack write down the number of receipts, the total spent and the largest one. That is a group-by with three aggregates. Throwing away the stacks with fewer than three receipts afterwards is the `having` step. The pile of individual receipts is gone, replaced by one summary line per shop.

### The formula

Let rows be split into groups $G_1, \dots, G_g$ by the key columns. For each group and aggregated column with the non-null values $v_1, \dots, v_m$:

$$
\text{count} = |G|, \qquad \text{sum} = \sum_{i=1}^{m} v_i, \qquad \text{mean} = \frac{1}{m}\sum_{i=1}^{m} v_i
$$

and $\min$ and $\max$ are the smallest and largest value. Nulls are skipped, so $m \le |G|$, and a group with $m = 0$ has no sum, mean, min or max.

- Splitting costs one pass through the data with a hash table from key to group: $O(n)$.
- The set of groups is the set of distinct key tuples, so adding a key column can only keep or increase the number of groups.
- `HAVING` filters groups after aggregating, while `WHERE` filters rows before grouping. A condition on an aggregate, such as `count > 5`, must be a `HAVING`.
- **Distinct count** is the size of the set of different values. It is not an average-style aggregate and cannot be combined across groups by adding.

### Null handling

SQL aggregates skip nulls except `COUNT(*)`, which counts rows. The average of a column with some missing values is the average of the present ones, which is a statistical choice as well as a database rule, as `02-missingness-patterns` explains.

### Group-by in machine learning code

Per-user and per-item statistics (average rating, purchase count, time since last event) are group-by aggregates joined back onto the training rows. Computed over the training split only, they are safe features. Computed over all the data, they leak the label into the features, the mistake discussed in `04-data-leakage`.

### How NumPy/PyTorch actually implements this

`pandas.DataFrame.groupby(keys).agg(...)` is this operation, with named aggregation `agg(total=('amount', 'sum'))` and `.filter` and `.query` give the `having` step. SQL's `GROUP BY` with `HAVING` is the same. `itertools.groupby` groups only adjacent rows, so the data must be sorted by the key first. `collections.defaultdict(list)` is the dict used here, `collections.Counter` counts, and `torch.scatter_reduce` and `np.add.at` aggregate by group on arrays.

## Explanation

`group_by` makes one pass over the rows, building a dict from the tuple of key values to the list of rows in that group. It then sorts the group tuples and, for each, builds an output dict starting with the key columns and then, for each requested aggregate, computes the result from the group's values. `_aggregate` drops `None` values, returns the row count for `count`, returns `None` when no values remain for the other functions, and otherwise applies the sum, mean, min or max, raising `ValueError` for an unknown name. `having` is a list comprehension over the grouped output. `count_distinct` puts the non-`None` values in a set and returns its size.
