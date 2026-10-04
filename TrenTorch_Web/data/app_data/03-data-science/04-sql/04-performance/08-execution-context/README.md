---
name: db-sql-perf-execution-context
title: 'Schema Introspection with PRAGMA'
tags: [db]
difficulty: Advanced
---

## Statement

Tools such as ORMs, migration scripts and admin screens need to ask the database about its own structure: which columns does a table have, what types are they, which one is the primary key? SQLite answers through `PRAGMA` commands, and many of them can also be used like tables inside a query.

Write a query that lists the structure of the `orders` table by reading `pragma_table_info('orders')`: return `name`, `type`, `"notnull"` and `pk` for every column.

### Constraints

- Columns, in order: `name`, `type`, `notnull`, `pk`
- Read from `pragma_table_info('orders')`
- One row per column of `orders`

### Hints

<details>
<summary>Hint 1</summary>

`SELECT ... FROM pragma_table_info('orders')` works like a table.

</details>

<details>
<summary>Hint 2</summary>

`notnull` is also a keyword, so quote it: `"notnull"`.

</details>

## Theory

### The simple version

`PRAGMA` commands let you ask the database about itself, such as which columns a table has, and they can be queried like tables.

### The database describes itself

`PRAGMA` statements read or change SQLite's settings and metadata. `PRAGMA table_info(orders)` lists a table's columns. The same information is available as a **table-valued function**, which you can filter, join and sort like any table:

```sql
SELECT name, type, "notnull", pk
FROM pragma_table_info('orders');
```

### Useful pragmas

| Pragma                    | Tells you                                               |
| ------------------------- | ------------------------------------------------------- |
| `table_info(t)`           | columns, types, NOT NULL, default, primary key position |
| `index_list(t)`           | indexes on a table                                      |
| `index_info(i)`           | columns inside an index                                 |
| `foreign_key_list(t)`     | foreign keys                                            |
| `page_size`, `cache_size` | storage and memory settings                             |

### Settings that change execution

Some pragmas change how queries run, for example `PRAGMA foreign_keys = ON` (enforce foreign keys) or `PRAGMA cache_size = ...`. They apply to the current connection ("execution context") only, so set them each time you connect.

### Combining with other tables

`SELECT m.name, p.name FROM sqlite_master m, pragma_table_info(m.name) p WHERE m.type = 'table'` lists every column of every table in one query.

## Explanation

`pragma_table_info('orders')` returns one row per column with its name, declared type, whether it is `NOT NULL` and its primary-key position (`id` has `pk = 1`). Because the test checks the exact rows and that the query reads the pragma, a typed-out list is rejected.
