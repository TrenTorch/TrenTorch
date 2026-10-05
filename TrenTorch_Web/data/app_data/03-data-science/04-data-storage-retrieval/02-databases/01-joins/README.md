---
name: data-storage-joins
title: Joins
tags: [databases, joins]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Data lives in separate tables for good reason: customers once, orders many times. Answering a question about both means **joining** them: pair every order with its customer through a shared key. The result is the same however it is computed, but the cost is not. Comparing every row of one table with every row of the other is quadratic and hopeless at scale. Two classic algorithms avoid it, one by building a hash table of one side and one by sorting both sides and walking them together. Choosing between them is a large part of what a query planner does. This question builds all three and shows they agree.

### From theory to code

Implement `nested_loop_join(left, right, key)`, the direct comparison of every pair, then `hash_join(left, right, key)`, which builds a hash table on one side, then `sort_merge_join(left, right, key)`, which sorts both sides and merges them. The signatures and docstrings are already in the editor.

### Constraints

- `left` and `right` are lists of rows, each row a dict. `key` is a column name present in every row of both tables, and key values are comparable and hashable (numbers or strings).
- All three functions perform an **inner join on equality**: for every pair `(l, r)` with `l[key] == r[key]`, the output has one row `{**l, **r}`. If a column name appears in both rows, the value from `r` wins. Rows with no match on the other side do not appear.
- Duplicate keys produce every combination: two left rows and three right rows with the same key give six output rows.
- Output order: `nested_loop_join` and `hash_join` return rows in order of the left table, and for each left row its matches in the order of the right table. `sort_merge_join` returns rows ordered by key ascending, then by left order, then by right order.
- `hash_join` must not compare every pair: build a dict from key to the list of right rows (in right-table order) and probe it once per left row. `sort_merge_join` must sort each side once by key (a stable sort) and advance two positions through them, not compare every pair. The input tables must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

A nested loop is two loops and an `if`. It is the reference answer the other two must agree with.

</details>

<details>
<summary>Hint 2</summary>

For the hash join, group the right rows by key first. Then each left row finds all its partners in one dictionary lookup.

</details>

<details>
<summary>Hint 3</summary>

For the merge join, once both sides are sorted, advance whichever side has the smaller key. When the keys are equal, find the whole run of equal keys on both sides and emit every combination of the two runs.

</details>

## Theory

### The simple version

Two guest lists, one with names and tables, one with names and meal choices. To find each guest's table and meal you could compare every name on one list with every name on the other, which is slow. Or you could index the second list by name once and look each guest up. Or you could sort both alphabetically and walk down them together, never going back. The three methods give the same answer and very different amounts of work.

### The formula

Let the tables have $n$ and $m$ rows. For an inner join on equality, the result contains one row for each pair with matching keys, so with a key value occurring $a$ times on the left and $b$ times on the right it contributes $a \cdot b$ rows.

| Algorithm       | How it works                                         | Cost                                     |
| --------------- | ---------------------------------------------------- | ---------------------------------------- |
| Nested loop     | test every pair                                      | $O(nm)$                                  |
| Hash join       | build a hash table on one side, probe with the other | $O(n + m + \text{output})$               |
| Sort-merge join | sort both sides, then merge                          | $O(n \log n + m \log m + \text{output})$ |

- The hash join needs memory for one whole side but no ordering. It only handles equality.
- The merge join handles inequality joins too, and costs nothing extra when the inputs are already sorted (as they are when read from a sorted index).
- The **build side** of a hash join is normally the smaller table, to keep the hash table small.
- The output size can be as large as $nm$ when all keys are equal, and no algorithm can beat the output size.

### Other kinds of joins

A **left outer join** also keeps left rows with no match, filling the right columns with nulls. Right and full outer joins are the mirror and the union. A **semi join** keeps left rows that have a match and a **cross join** is every pair with no condition. All are small variations of the loops built here.

### How a planner chooses

A query planner estimates table sizes and whether each side is sorted or indexed, then picks the cheapest algorithm. A tiny table joined against an indexed one uses a nested loop with index lookups. Two large unsorted tables use a hash join. Two large tables already sorted on the key use a merge join.

### How NumPy/PyTorch actually implements this

`pandas.merge(left, right, on=key, how='inner')` is a join, using a hash-based algorithm internally and offering `how='left'`, `'right'` and `'outer'`. SQL's `JOIN ... ON` is the same operation, and database engines implement all three algorithms. `polars.DataFrame.join` and `duckdb` do the same at columnar speed, and `torch.searchsorted` plus indexing joins sorted tensors.

## Explanation

`nested_loop_join` tests every left row against every right row, in table order, and appends a merged row for each match, which defines the reference output. `hash_join` groups the right rows by key into a dict of lists, keeping right order within a key, then walks the left rows in order and looks each key up once, emitting the merged rows for every partner. `sort_merge_join` stably sorts each side by key, then keeps one position in each: when the left key is smaller it advances left, when larger it advances right, and when equal it finds the end of the run of equal keys on both sides and emits the product of the two runs before moving past them.
