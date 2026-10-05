---
name: data-science-pandas-boolean-filtering
title: Boolean Masks & Filtering
tags: [data-science, pandas, filtering]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Most of exploratory analysis is asking a question of a table and keeping the rows that answer it: customers over 30, orders from three cities, readings outside the normal range, rows where a value is _not_ missing. In pandas a question like that is a **boolean mask**, a column of `True`/`False` the same length as the table, and keeping the rows is just indexing with the mask.

The mask itself is built from comparisons, and combining comparisons has two traps that cost beginners hours. Python's `and`, `or` and `not` do not work on arrays (they ask for one truth value from many), so pandas uses `&`, `|` and `~`, and because of operator precedence every comparison must be wrapped in parentheses. The second trap is `NaN`: it is neither greater than nor less than anything, so a comparison against it is `False`, and `~(x > 5)` is `True` for a missing value, which is rarely what you meant.

### From theory to code

Implement `in_range(df, column, low, high)`, `from_cities_and_old_enough(df, cities, min_age)`, `any_extreme(df, column, low, high)`, `exclude_values(df, column, values)` and `complete_rows(df, columns)`. The signatures and docstrings are already in the editor.

### Constraints

- Every function returns the selected rows of `df` with their **original index labels and column order**, not renumbered.
- `in_range(df, column, low, high)` keeps rows where `low <= column <= high` (both ends included). Rows where the column is `NaN` are dropped.
- `from_cities_and_old_enough(df, cities, min_age)` keeps rows whose `city` is in `cities` **and** whose `age >= min_age`.
- `any_extreme(df, column, low, high)` keeps rows where `column < low` **or** `column > high`. A `NaN` is not extreme, so those rows are dropped.
- `exclude_values(df, column, values)` keeps rows whose `column` is **not** in `values`. A row where the column is `NaN` is kept (it is not in `values`).
- `complete_rows(df, columns)` keeps rows that have no missing value in any of the listed `columns`.
- Do not use `DataFrame.query`.

### Hints

<details>
<summary>Hint 1</summary>

`s.between(low, high)` is inclusive on both sides by default.

</details>

<details>
<summary>Hint 2</summary>

Wrap each comparison in parentheses before combining: `(df.a > 1) & (df.b < 2)`.

</details>

<details>
<summary>Hint 3</summary>

`s.isin(values)` gives a mask, and `~mask` flips it. `df[columns].notna().all(axis=1)` checks every listed column at once.

</details>

## Theory

### The simple version

A filter is a stencil: lay a sheet with holes on the table and only the rows under a hole show through. The sheet is a column of `True` and `False`, one per row. Comparisons make stencils, and `&`, `|`, `~` combine stencils: both holes (`&`), either hole (`|`), the opposite of the sheet (`~`).

### Building a mask

```python
mask = df["age"] >= 30                    # one comparison: a boolean Series
mask = (df["age"] >= 30) & (df["city"] == "Pune")
rows = df[mask]                           # or df.loc[mask]
```

The mask has the same index as the frame, so `df[mask]` keeps exactly the rows labelled `True`, in their original order and with their original labels.

### Why `&` and parentheses

`and` asks Python for a single truth value of a whole column, which is ambiguous, so pandas raises `ValueError: The truth value of a Series is ambiguous`. The bitwise operators are applied element by element. They also bind _tighter_ than comparison operators, so `df.a > 1 & df.b < 2` parses as `df.a > (1 & df.b) < 2`. Always parenthesise each comparison.

### Missing values in comparisons

For `NaN`, every ordering comparison is `False` and `!=` is `True`:

| expression        | on `NaN` |
| ----------------- | -------- |
| `x > 5`           | `False`  |
| `x <= 5`          | `False`  |
| `~(x > 5)`        | `True`   |
| `x.isin([1, 2])`  | `False`  |
| `x.between(1, 9)` | `False`  |

So `~(x > 5)` is **not** the same as `x <= 5`: it also keeps the missing rows. State what you want for missing values out loud, then pick the expression that does it. `df.notna()` / `df.isna()` test for missing directly.

### Membership and ranges

`isin` replaces a chain of `==` joined by `|` and is faster. `between(low, high)` is `(x >= low) & (x <= high)`, inclusive by default, with `inclusive="neither"`, `"left"` or `"right"` to change the ends.

### How pandas actually implements this

Comparisons are vectorised NumPy operations on the column's array, producing a boolean array wrapped back into a Series with the same index. `df[mask]` converts the mask to integer positions (`np.flatnonzero`) and takes those rows from each column block. Nothing loops in Python, which is why a mask over a million rows is milliseconds.

## Explanation

`in_range` is `df[df[column].between(low, high)]`; `between` is inclusive and false for `NaN`. `from_cities_and_old_enough` combines `isin` with a comparison using `&` and parentheses. `any_extreme` joins two comparisons with `|`; both are false for `NaN`, so missing values are dropped. `exclude_values` negates `isin` with `~`, and since `isin` is false for `NaN` the negation keeps those rows, as the contract requires. `complete_rows` checks `notna()` on the listed columns and requires all of them with `all(axis=1)`. Every result is a row selection, so the original labels survive.
