---
name: data-storage-query-pipeline
title: Query Execution Pipeline
tags: [databases, query-execution]
difficulty: Advanced
---

## Statement

### The problem, from first principles

A SQL query such as `SELECT name FROM users WHERE age > 30 ORDER BY name LIMIT 10` looks like one command and runs as a pipeline of small steps: scan the table, keep the rows that pass the filter, pick the columns, sort, stop after ten. Each step takes a stream of rows in and hands a stream of rows out, and connecting them lets a database answer a query on a billion rows while holding only a few in memory. The key idea is **laziness**: a step does no work until the step after it asks for a row, so `LIMIT 10` reads only as much of the table as it needs. This question builds the operators as Python generators and composes them into a query.

### From theory to code

Implement the operators `scan(table)`, `filter_rows(rows, predicate)`, `project(rows, columns)`, `order_by(rows, column, descending)` and `limit(rows, n)`, each taking and returning an iterable of row dicts, then `run_query(table, where, columns, order_column, descending, row_limit)`, which chains them. The signatures and docstrings are already in the editor.

### Constraints

- A row is a dict. `scan`, `filter_rows`, `project` and `limit` must be **generators** (they use `yield`) that pull rows from their input one at a time. They must not build the full list of rows.
- `scan(table)` yields the rows of a list in order. `filter_rows(rows, predicate)` yields only the rows for which `predicate(row)` is true. `project(rows, columns)` yields a new dict per row holding only the listed columns, in the order listed.
- `limit(rows, n)` yields at most `n` rows and stops **without pulling any more rows from its input** once it has yielded `n` (for `n <= 0` it pulls none).
- `order_by(rows, column, descending=False)` is a **blocking** operator: it must read all input before yielding anything. It yields the rows sorted by `row[column]`, with `descending=True` reversing the order. The sort is stable, so rows with equal keys keep their input order, in descending order as well. Rows whose value is `None` sort last in both directions.
- `run_query(table, where, columns, order_column, descending, row_limit)` returns a **list**. The steps run in the order scan, filter (if `where` is not `None`), sort (if `order_column` is not `None`), limit (if `row_limit` is not `None`), project (if `columns` is not `None`). Sorting and limiting happen **before** projection, so the sort column need not be among the projected columns.
- Input rows and the table must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

A generator function runs only when something asks it for the next value. Writing `for row in rows: if predicate(row): yield row` is a complete lazy filter.

</details>

<details>
<summary>Hint 2</summary>

Sorting cannot be lazy, since the first output row may be the last input row. That is why `LIMIT` after a sort still reads everything, but `LIMIT` with no sort reads only `n` rows.

</details>

<details>
<summary>Hint 3</summary>

For descending order with stability, sort by a key that places `None` last, then reverse only the non-null block's key order using `reverse=True`, which preserves the order of equal elements.

</details>

## Theory

### The simple version

An assembly line where each worker does one job and passes the item along. The first worker takes parts from a bin, the second throws out defective ones, the third paints, the last stops after the tenth item. Nobody waits for the whole bin to be processed. When the last worker has ten items the line stops, and the rest of the bin is never touched. The one exception is a worker who has to see every item before passing any on, like someone sorting finished items by size.

### The formula

Each operator is a function from a stream of rows to a stream of rows, and a query is their composition:

$$
\text{result} = \text{project}\ \circ\ \text{limit}\ \circ\ \text{order\_by}\ \circ\ \text{filter}\ \circ\ \text{scan}\ (\text{table})
$$

This is the **iterator** (or _Volcano_) model: each operator exposes "give me the next row" and calls the same on its input.

| Operator              | Lazy?                  | Memory | Time                        |
| --------------------- | ---------------------- | ------ | --------------------------- |
| scan, filter, project | yes, row at a time     | $O(1)$ | $O(n)$                      |
| limit                 | yes, stops early       | $O(1)$ | $O(\min(n, k))$ rows pulled |
| order by              | no, must see every row | $O(n)$ | $O(n \log n)$               |

- **Pushdown**: filtering as early as possible shrinks what later operators handle. Limiting before projecting avoids building rows that are then discarded.
- A **blocking** operator (sort, group-by, hash-join build side) breaks the pipeline: nothing flows past it until its input is exhausted.
- Order of operators matters for correctness too: filter must come before limit (otherwise it would filter only the first $k$ rows), and sort before limit (otherwise it would sort an arbitrary $k$ rows).

### Query planning

A SQL engine parses the text into a tree of these operators, then **optimizes** the tree: pushes filters toward the scan, picks indexes (`04-btree-index`) and join algorithms (`01-joins`), and chooses the order of operations by estimated cost. `EXPLAIN` shows the chosen plan.

### Generators in data code

The same pattern streams files too large for memory: read a line, parse, filter, write. Python generators, `itertools`, PyTorch's `DataLoader` and TensorFlow's `tf.data` pipelines all use it and `03-generators-yield` in the Python track explains the mechanics.

### How NumPy/PyTorch actually implements this

`sqlite3` and DuckDB run exactly this model in C. In Python, generator expressions, `filter`, `map` and `itertools.islice` are lazy `filter_rows`, `project` and `limit`, while `sorted()` is the blocking `order_by`. `pandas.DataFrame.query(...).sort_values(...).head(n)[columns]` is the same pipeline evaluated eagerly, one whole table at a time. `heapq.nsmallest` implements `ORDER BY ... LIMIT` without sorting everything, using the heap from `03-heaps-top-k`.

## Explanation

`scan`, `filter_rows`, `project` and `limit` are generator functions: each loops over its input and `yield`s, so no row is produced until the next operator asks for one. `limit` counts the rows it has yielded and returns as soon as it reaches `n`, before asking the input for another, which is what keeps the table from being read further. `order_by` is the one blocking operator: it collects every input row into a list, separates rows whose sort value is `None` so they can be placed last, sorts the rest with `sorted(..., reverse=descending)`, which is stable, and yields the sorted rows followed by the null rows. `run_query` threads the operators together in the order scan, filter, sort, limit, project and returns the list of results.
