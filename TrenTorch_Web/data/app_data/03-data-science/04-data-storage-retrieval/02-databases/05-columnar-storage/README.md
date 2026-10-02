---
name: data-storage-columnar-storage
title: 'Row & Columnar Storage'
tags: [databases, storage]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A table is a grid, and a disk holds a line of bytes, so somebody has to decide how to lay the grid out along the line. **Row storage** writes one whole record after another, which is ideal for fetching or changing a single customer. **Columnar storage** writes all of one column, then all of the next, which is ideal for analytics: the average of one column over a hundred million rows touches only that column, and a column of similar values also compresses far better than a mix of types. The choice shapes the speed of every query, and almost every analytics engine and every dataframe library is columnar. This question builds both layouts, a simple compression that columns make possible and a cost model that shows why the choice matters.

### From theory to code

Implement `rows_to_columns(rows)` and `columns_to_rows(columns)`, which convert between the two layouts, then `run_length_encode(values)` and `run_length_decode(pairs)`, a compression that exploits repeated values, then `bytes_scanned(layout, num_rows, num_columns, columns_needed, value_bytes)`, the amount of data a query reads in each layout. The signatures and docstrings are already in the editor.

### Constraints

- A **row table** is a list of dicts that all have the same keys in the same order. A **column table** is a dict mapping each column name to the list of that column's values, in row order, with columns in the same order as the keys of the rows.
- `rows_to_columns(rows)` returns the column table. For an empty list of rows it returns `{}`. `columns_to_rows(columns)` returns the list of row dicts, with keys in the order of `columns`. An empty column table gives `[]`. Converting there and back must return the original rows.
- `run_length_encode(values)` returns a list of `(value, count)` pairs, one per **run** of equal consecutive values, in order. `run_length_decode(pairs)` returns the original list. An empty list encodes to `[]`.
- `bytes_scanned(layout, num_rows, num_columns, columns_needed, value_bytes)` returns an int. For `layout == "row"` a query must read every value of every row: `num_rows * num_columns * value_bytes`. For `layout == "column"` it reads only the needed columns: `num_rows * columns_needed * value_bytes`. Any other layout raises `ValueError`.
- Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

Going from rows to columns is a transpose. For each column name collect that key from every row, in order.

</details>

<details>
<summary>Hint 2</summary>

A run is a maximal stretch of equal neighbours, so a new run starts exactly when a value differs from the one before it.

</details>

<details>
<summary>Hint 3</summary>

A row store has no way to read one column without also reading the rest of the record, because the values of a row sit next to each other on disk.

</details>

## Theory

### The simple version

A school keeps one folder per student, with that student's name, grade, address and everything else. To find one student's address the folder is perfect. To find the average age of the whole school the secretary has to open every folder. If instead the school kept one long list of all the ages, another of all the names, and so on, the average age needs only the list of ages, and that list, being all numbers of similar size, is also easy to squeeze. Folders are rows and the lists are columns.

### The formula

For a table with $n$ rows, $c$ columns and $b$ bytes per value, a query that needs $q$ of the columns reads

$$
\text{row store: } n\,c\,b \text{ bytes}, \qquad \text{column store: } n\,q\,b \text{ bytes}
$$

so the column layout saves a factor of $c/q$ on analytic scans. A point lookup of one whole record is the opposite case: a row store reads one contiguous record, while a column store must visit $c$ separate places.

**Run-length encoding** replaces each run of equal values by one pair $(\text{value}, \text{count})$:

$$
[\mathrm{A}, \mathrm{A}, \mathrm{A}, \mathrm{B}, \mathrm{B}, \mathrm{A}] \ \longrightarrow\ [(\mathrm{A}, 3), (\mathrm{B}, 2), (\mathrm{A}, 1)]
$$

- Its size is proportional to the number of runs, so it shrinks a column a great deal when values repeat (a sorted column, a status flag, a country code) and can **grow** a column with no repeats.
- Columns compress better than rows because a column holds values of one type with similar distributions. Sorting the table by a low-cardinality column creates long runs.
- Row stores suit transactional work (many small reads and writes of whole records). Column stores suit analytics (few columns, many rows).

### Other column encodings

**Dictionary encoding** replaces repeated strings by small integer codes. **Delta encoding** stores differences between neighbours, which is small for timestamps and sorted IDs. **Bit-packing** stores integers in the minimum number of bits. Real columnar formats such as Parquet combine these with a general-purpose compressor.

### In Python data work

A pandas DataFrame and a NumPy structured table are column stores: each column is one contiguous array, which is why summing a column is fast and why iterating row by row is slow. Reading only the needed columns from a Parquet file is column pruning, the same saving as the cost model above.

### How NumPy/PyTorch actually implements this

`pandas.DataFrame` stores data column by column internally, `DataFrame.to_dict('list')` is `rows_to_columns` and `to_dict('records')` is `columns_to_rows`. `pyarrow` and Parquet are the standard columnar file format and memory layout, and `DuckDB`, `ClickHouse` and `BigQuery` are columnar engines. `itertools.groupby` groups runs, which is the heart of `run_length_encode`, and `numpy.diff` plus `np.flatnonzero` finds run boundaries on arrays. `sqlite3` and PostgreSQL are row stores.

## Explanation

`rows_to_columns` takes the column names from the first row and builds each column's list by pulling that key out of every row, which is a transpose. `columns_to_rows` zips the column lists together, giving one dict per position with the keys in the order of the column table. `run_length_encode` walks the values keeping the current value and its count, closing the run and starting a new one whenever the next value differs, and `run_length_decode` repeats each value by its count. `bytes_scanned` multiplies the number of rows and the number of columns that must be read, which is every column for the row layout and only the needed ones for the column layout, by the width of one value.
