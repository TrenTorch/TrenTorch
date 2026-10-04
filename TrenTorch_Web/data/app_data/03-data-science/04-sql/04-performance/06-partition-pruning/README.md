---
name: db-sql-perf-partition-pruning
title: 'Partition Pruning with Range Predicates'
tags: [db]
difficulty: Advanced
---

## Statement

The `events` table holds two years of data (6,000 rows) with an index `idx_events_date` on `event_date` (text such as `'2024-03-15'`). Reports usually ask about one month.

A first attempt is:

```sql
SELECT COUNT(*) FROM events WHERE strftime('%Y-%m', event_date) = '2024-03';
```

It is correct but slow: the function hides the column from the index, so SQLite scans all 6,000 rows. Rewrite it so the engine can read only the March slice of the index (the same idea as _partition pruning_ in partitioned databases).

Return the number of events whose `event_date` is in March 2024.

### Constraints

- Return a single count
- Compare `event_date` itself with a start date and an end date; do not call functions on it
- The plan must be a `SEARCH` using `idx_events_date`

### Hints

<details>
<summary>Hint 1</summary>

A range `>= '2024-03-01' AND < '2024-04-01'` covers exactly March.

</details>

<details>
<summary>Hint 2</summary>

Using a half-open range (`<` next month) also works for values with a time part.

</details>

## Theory

### The simple version

If data is sorted by a key, a query on a range of that key can skip everything outside the range. Wrapping the column in a function prevents that.

### Partition pruning in one sentence

If the data is divided into pieces by a key (partitions, or the sorted order of an index), a query that filters on that key can **skip** the pieces that cannot contain matches.

### SQLite has no partitions: the index does the same job

An index on `event_date` keeps rows sorted by date, so a date range maps to one contiguous slice:

```sql
SELECT COUNT(*) FROM events
WHERE event_date >= '2024-03-01' AND event_date < '2024-04-01';
-- SEARCH events USING COVERING INDEX idx_events_date (event_date>? AND event_date<?)
```

### Sargable predicates

A predicate is _sargable_ (Search ARGument able) when the planner can use an index for it. Applying a function to the column breaks that:

| Not sargable                                | Sargable                                                   |
| ------------------------------------------- | ---------------------------------------------------------- |
| `strftime('%Y-%m', event_date) = '2024-03'` | `event_date >= '2024-03-01' AND event_date < '2024-04-01'` |
| `substr(name, 1, 3) = 'abc'`                | `name >= 'abc' AND name < 'abd'`                           |
| `amount + 10 > 100`                         | `amount > 90`                                              |

### Half-open ranges

`>= start AND < next_start` works for dates with or without a time part and never double counts a boundary.

## Explanation

Comparing the bare column with a range lets SQLite do a range search on `idx_events_date`, reading only March. The function version cannot use the index and scans every row. The tests reject functions on the column and check the plan.
