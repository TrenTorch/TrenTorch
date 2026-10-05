---
name: data-science-pandas-pivot-crosstab
title: Pivot Tables, Crosstabs & Reshaping
tags: [data-science, pandas, pivot, reshape]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A table of one row per sale is the right shape for storing data and the wrong shape for reading it. A manager wants regions down the side and quarters across the top, with the revenue where they cross. That rearrangement is a **pivot**, and its mirror image, taking such a grid and turning it back into one row per measurement, is a **melt**. Between them they let data move between the _long_ form that analysis tools like and the _wide_ form that people read.

This question builds the four reshapes that come up most: a pivot that sums a measure and fills empty cells, a grid with totals, a count table of two categorical columns (a crosstab) and the row-percentage version of it, and the melt back to long form.

### From theory to code

Implement `revenue_pivot(df)`, `add_totals(grid)`, `count_table(df, row, col)`, `row_percentages(table)` and `to_long(wide, id_col, var_name, value_name)`. The signatures and docstrings are already in the editor.

### Constraints

- `revenue_pivot(df)` takes a frame with columns `region`, `quarter`, `revenue` (one or more rows per region and quarter) and returns a grid with the regions as the index and the quarters as the columns, each cell the **sum** of `revenue` for that pair, `0` where there are no rows. Both axes are sorted ascending.
- `add_totals(grid)` returns a **new** grid with one extra row labelled `"Total"` (column sums) at the bottom and one extra column labelled `"Total"` (row sums) at the right, including the grand total in the corner. The input is not changed.
- `count_table(df, row, col)` returns the number of rows for every pair of values of the columns `row` and `col`: distinct values of `row` down the side, of `col` across the top, both sorted ascending, `0` where a pair never occurs.
- `row_percentages(table)` returns the table with every cell turned into the percentage of its **row** total (each row sums to 100). Rows whose total is zero become `NaN`.
- `to_long(wide, id_col, var_name, value_name)` melts every column other than `id_col` into rows: the result has the columns `id_col`, `var_name`, `value_name`, ordered by `id_col` in the original row order and, within one id, by the original column order. Fresh `0..n-1` index.

### Hints

<details>
<summary>Hint 1</summary>

`pivot_table` aggregates duplicate cells (the default is the mean, so say `aggfunc`) and takes `fill_value`.

</details>

<details>
<summary>Hint 2</summary>

`pd.crosstab(a, b)` counts pairs and sorts both axes. Dividing a table by its row sums with `div(..., axis=0)` divides each row by its own total.

</details>

<details>
<summary>Hint 3</summary>

`melt` stacks one block of rows per column, so every id repeats once per column. A stable sort by the id column puts each id's rows together without reordering its columns.

</details>

## Theory

### The simple version

A bank statement lists one transaction per line (long). A budget spreadsheet has one row per category and one column per month (wide). Going long to wide _groups and spreads_: for each (category, month) pair, add up the transactions. Going wide to long _unpivots_: every cell becomes its own line again, tagged with its row and column labels.

<div class="tt-widget" data-widget="data-science-pandas-pivot-crosstab"></div>

### Long and wide

| Form        | One row is                    | Good for                                    |
| ----------- | ----------------------------- | ------------------------------------------- |
| long (tidy) | one observation               | filtering, grouping, plotting libraries     |
| wide        | one entity, many measurements | reading, spreadsheets, correlation matrices |

### Pivot = groupby + reshape

A pivot table is a `groupby` on two keys followed by moving the second key from the index to the columns:

```python
df.pivot_table(index="region", columns="quarter", values="revenue",
               aggfunc="sum", fill_value=0)
# same as: df.groupby(["region", "quarter"])["revenue"].sum().unstack(fill_value=0)
```

`pivot` (without `_table`) does no aggregation and raises if a (row, column) pair repeats, which is a useful sanity check. `pivot_table` aggregates duplicates, and its default `aggfunc` is the **mean**, a common source of "the totals look too small".

### Crosstabs and percentages

`pd.crosstab(df["a"], df["b"])` is a pivot whose cells are _counts_. Normalising by row answers "of the customers in each region, what share chose each plan":

$$
p_{ij} = 100\cdot\frac{n_{ij}}{\sum_{j'} n_{ij'}}
$$

A row with no observations divides $0$ by $0$, which is `NaN`, an honest "no data".

### Totals

`margins=True` adds an `All` row and column. Doing it by hand, with the row sums as a new column and the column sums as a new row, shows what a margin is, and the corner cell is the sum of everything.

### How pandas actually implements this

`pivot_table` is a `groupby` followed by `unstack`, which rearranges the multi-level index into columns using integer codes (no Python loop). `melt` is the opposite: it repeats the id columns once per value column and concatenates the blocks. `crosstab` builds the two key arrays and calls `pivot_table` with `aggfunc="count"`.

## Explanation

`revenue_pivot` calls `pivot_table` with `aggfunc="sum"` and `fill_value=0`, and sorts both axes. `add_totals` copies the grid, adds a `"Total"` column of row sums, then a `"Total"` row of column sums over that extended grid so the corner holds the grand total. `count_table` is `pd.crosstab`, whose axes are already sorted. `row_percentages` divides each row by its own sum with `div(axis=0)` and multiplies by 100, and zero-sum rows become `NaN`. `to_long` melts the non-id columns and stable-sorts by id, so each id's rows stay in the original column order.
