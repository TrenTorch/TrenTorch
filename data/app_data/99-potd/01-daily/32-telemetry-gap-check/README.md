---
name: potd-telemetry-gap-check
title: 'THE TELEMETRY GAP CHECK'
tags: [data-processing]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Data Processing

---

### Story

A Databricks ETL job needs to flag which columns have missing telemetry before any imputation or
modeling touches the table: the single most common first step in any real data pipeline.

---

### The Problem

No math here: count missing (`NA`) entries per column.

### Input Format

```
n k
col_1_name ... col_k_name
row_1 (k values, `NA` denotes missing)
...
row_n
```

### Output Format

`col_name missing_count`, one line per column, in the given column order.

### Constraints

- `1 <= n <= 10^5`, `1 <= k <= 100`
- Time limit: 1.0 second.

---

### Example

**Input**

```
4 2
a b
1 NA
NA NA
3 1
NA 2
```

**Output**

```
a 2
b 2
```

## Theory

### The simple version

Before you can trust any model or any chart, you need to know where your data has holes. This just counts, column by column, how many values are missing.

### The sentinel is exact and literal

Only the exact literal string `NA` counts as missing. A near-miss like `"N/A"` or `"null"` must
**not** be counted: over-generalizing the missing-value check to any string that looks like a
missing marker silently miscounts columns that use a different marker on purpose, or that legitimately
contain the text `"null"` as real data.

### Zero is still printed

A column with zero missing values still gets a line in the output with count `0`: the output always
has exactly `k` lines, in the given column order, never fewer.

### A column entirely missing is not special

If every row's value in a column is `NA`, its count is simply `n`, computed the same way as any
other column.

## Explanation

`count_missing_per_column` walks the `n x k` grid of raw string values and, for each column, counts
how many of its `n` entries equal the literal string `"NA"` exactly (`== "NA"`, not a substring or
case-insensitive check), returning the counts in the same order as the given column names. Because
the comparison is an exact string equality, `"N/A"` and `"null"` never match, and a column of all
`"NA"` values ends up with count `n` from the same counting logic every other column uses.
