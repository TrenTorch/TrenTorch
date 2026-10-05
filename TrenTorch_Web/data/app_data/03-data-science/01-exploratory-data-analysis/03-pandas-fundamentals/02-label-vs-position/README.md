---
name: data-science-pandas-label-vs-position
title: Label vs Position Selection
tags: [data-science, pandas, indexing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A DataFrame can be addressed in two different languages. By **label**: the row called `"2024-03-01"`, the column called `"price"`. By **position**: the third row, the second column. The two agree only when the index happens to be `0, 1, 2, ...`, and the moment rows are filtered, sorted or re-indexed they stop agreeing. A bug that looks like "I selected the wrong rows" is nearly always a label used where a position was meant, or the reverse.

This question implements the selections you reach for every day, and each one is defined so you must know which language it speaks. They also settle two sharp edges: label slices include their end, position slices do not, and assigning into a _selection_ can silently change nothing or change the original frame, so the safe pattern is to work on a copy.

### From theory to code

Implement `rows_by_label(df, start, stop)`, `rows_by_position(df, start, stop)`, `cell(df, row_label, column)`, `numeric_columns(df)` and `with_value_where(df, mask, column, value)`. The signatures and docstrings are already in the editor.

### Constraints

- `df` has a unique, sorted-or-unsorted index of any type and unique column names.
- `rows_by_label(df, start, stop)` returns the rows from label `start` to label `stop` **inclusive of both ends**, in the frame's own order. Both labels exist in the index.
- `rows_by_position(df, start, stop)` returns rows at positions `start` up to but **not including** `stop`, like a Python slice.
- `cell(df, row_label, column)` returns the single value at that row label and column name.
- `numeric_columns(df)` returns the names of the columns holding numbers (integers or floats, not booleans), in the frame's column order, as a list.
- `with_value_where(df, mask, column, value)` returns a **new** frame in which `column` is set to `value` on the rows where the boolean `mask` is true. `df` itself is never changed.

### Hints

<details>
<summary>Hint 1</summary>

`.loc` is the label door and `.iloc` is the position door. Which one treats the end of a slice as included?

</details>

<details>
<summary>Hint 2</summary>

`select_dtypes` can pick columns by kind, and `'number'` is a kind it understands.

</details>

<details>
<summary>Hint 3</summary>

Copy first, then assign with `.loc[mask, column] = value`. Assigning to the original would change the caller's data.

</details>

## Theory

### The simple version

A hotel has room _numbers_ (labels) and a fixed _order along the corridor_ (positions). "Room 12" and "the 12th room" are the same only if numbering starts at 1 and never skips. Once some rooms are closed for renovation, they point at different doors. `.loc` takes room numbers, `.iloc` takes places in the corridor, and mixing them up opens the wrong door without any error.

### Two selection languages

|              | `.loc`           | `.iloc`                     |
| ------------ | ---------------- | --------------------------- |
| Speaks       | labels           | integer positions           |
| Slice `a:b`  | **includes** `b` | excludes `b`, like Python   |
| Missing key  | `KeyError`       | `IndexError`                |
| Boolean mask | allowed          | allowed (array, not Series) |

Label slices include the end because labels have no natural "next one": excluding `"2024-03-31"` would need to know what comes after it. A positional slice can say "stop before position 5" because positions are consecutive integers.

### One cell, fast

`df.at[row, col]` and `df.iat[i, j]` return a single scalar and are quicker than `loc` and `iloc` because they skip the machinery for building sub-frames. The result is the stored value itself, not a Series.

### Selecting by type

A DataFrame stores each column with its own dtype. `df.select_dtypes(include="number")` returns the columns whose dtype is integer or float (booleans are a separate kind), which is how code picks "the columns I can average" without listing them by hand.

### Setting values safely

`df[mask]["col"] = v` is the famous trap: `df[mask]` may build a copy, so the assignment goes to a temporary and the original stays unchanged (pandas warns with `SettingWithCopyWarning`, and under copy-on-write semantics it simply never reaches the original). The pattern that always means what it says is one `.loc` with both the rows and the column, applied to a frame you are allowed to change:

```python
out = df.copy()
out.loc[mask, "col"] = v
```

### How pandas actually implements this

Each indexer is a small object (`_LocIndexer`, `_iLocIndexer`) whose `__getitem__` translates the key into integer positions through the index's `get_loc` / `slice_indexer`, then asks the block manager for those positions. `loc` goes through the index hash table, `iloc` skips it, and `at`/`iat` take a fast path straight to one cell.

## Explanation

`rows_by_label` uses `df.loc[start:stop]`, whose slice includes both labels; `rows_by_position` uses `df.iloc[start:stop]`, whose slice stops before `stop`, and the two return different rows as soon as the index is not `0..n-1`. `cell` is `df.at[row_label, column]`. `numeric_columns` selects dtype `number` and lists the names, which leaves out booleans and text. `with_value_where` copies the frame, assigns through one `.loc[mask, column]` and returns the copy, so the caller's frame is untouched.
