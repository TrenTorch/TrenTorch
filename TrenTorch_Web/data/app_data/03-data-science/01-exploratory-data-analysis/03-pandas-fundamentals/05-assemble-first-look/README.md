---
name: data-science-pandas-assemble-first-look
title: Assemble: A First Look at a Dataset
tags: [data-science, pandas, eda, assemble]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The first thing anyone does with a new table is look at it, and the same handful of questions come up every time. How big is it? Which columns have holes, and how many? Are there repeated rows? For the numeric columns, what are the centre, the spread and the extremes? For the categorical ones, how many different values are there, and which one is most common? Notebooks answer with `df.info()` and `df.describe()` and a handful of `value_counts()` calls, and a person reads the output.

A program cannot read a printout, so this question builds the same first look as **data**: one dictionary a test (or a monitoring job, or a report) can check. It combines what the previous questions taught: dtypes, missing values, boolean logic, and sorting.

### From theory to code

Implement `profile(df)`. The signature and docstring are already in the editor.

### Constraints

- `profile(df)` returns a dict with exactly these keys: `n_rows`, `n_cols`, `missing`, `n_duplicate_rows`, `numeric`, `categorical`.
- `n_rows` and `n_cols` are Python `int`s. `missing` maps **every** column name to its number of missing values (an `int`), in column order.
- `n_duplicate_rows` is the number of rows that repeat an earlier row exactly (the first occurrence is not counted).
- A column is **numeric** if its dtype is integer or float (booleans are not numeric). Every other column is **categorical**.
- `numeric` maps each numeric column to a dict `{"mean", "std", "min", "max"}` of Python floats computed over the non-missing values. `std` is the **sample** standard deviation (divide by `n - 1`). If a column has fewer than 2 non-missing values, `std` is `nan`; if it has none, all four are `nan`.
- `categorical` maps each categorical column to `{"n_unique", "top", "top_count"}`: the number of distinct non-missing values, the most frequent non-missing value, and how many times it occurs. If several values tie for most frequent, `top` is the **smallest** of them. If the column has no non-missing values, `top` is `None` and `top_count` is `0`.

### Hints

<details>
<summary>Hint 1</summary>

`Series.isna().sum()` counts missing values, and `df.duplicated()` marks repeated rows.

</details>

<details>
<summary>Hint 2</summary>

`pd.api.types.is_numeric_dtype` is true for booleans too, so exclude them explicitly.

</details>

<details>
<summary>Hint 3</summary>

`value_counts()` sorts by count but its order among ties is not a contract you should rely on. Find the maximum count and take the smallest value that has it.

</details>

## Theory

### The simple version

A first look at a table is a doctor's intake form: height, weight, blood pressure for the measurements, a short list of yes/no and category answers for everything else, plus a note of which boxes were left blank. The numeric columns get _summary numbers_; the label columns get _counts_. Doing it as a dictionary makes the form something a program can store, compare and alert on.

### What each summary says

For a numeric column with values $x_1,\dots,x_n$ (missing ones removed):

$$
\bar{x} = \frac{1}{n}\sum_i x_i, \qquad s = \sqrt{\frac{1}{n-1}\sum_i (x_i-\bar{x})^2}
$$

The mean locates the centre and the **sample** standard deviation $s$ measures spread, dividing by $n-1$ because the mean was itself estimated from the same data. Minimum and maximum bound the range and catch impossible values (an age of 400, a negative price). If $n<2$ the spread is not defined, and returning `nan` says so honestly instead of `0`, which would claim certainty.

### Categorical columns

A count of distinct values separates a flag (2), a category (dozens) and an identifier (about as many as rows), and the most frequent value with its count shows how skewed the column is. Ties need a rule or the answer depends on row order; "smallest value" is arbitrary but reproducible.

### Missing data and duplicates

A column that is 40% missing and one that is 0% missing need different treatment, so the count per column is the most useful single number in a first look. Exact duplicate rows usually mean a join or a load ran twice. They are cheap to count and expensive to miss.

### Types decide everything

A column of digits stored as text is categorical to pandas even though it is numeric to a human. Looking at dtypes first is how that kind of problem surfaces: `n_unique` equal to `n_rows` on a "numeric" column is a clue it is really an identifier.

### How pandas actually implements this

`DataFrame.describe()` does the same split: it summarises numeric columns with `count/mean/std/min/quartiles/max` and, for object columns, `count/unique/top/freq`. `std` defaults to `ddof=1`, and `value_counts()` is a hash-table count. `isna()` is a vectorised check against `NaN`/`None`/`NaT`, and `duplicated()` hashes whole rows.

## Explanation

`profile` loops over the columns once, sorting each into numeric or categorical by dtype (excluding booleans from numeric). Missing counts come from `isna().sum()` cast to `int`. For a numeric column it drops the missing values and returns the mean, the `ddof=1` standard deviation (`nan` when there is a single value), the minimum and the maximum, all as Python floats. For a categorical column it counts the non-missing values, finds the highest count, and takes the smallest value among those that reach it so ties are deterministic. Duplicate rows come from `df.duplicated().sum()`, which does not count first occurrences.
