---
name: db-sql-rank
title: 'RANK: Window Function with Gaps'
tags: [db]
difficulty: Advanced
---

## Statement

Rank users by age **within their region**, oldest first (rank 1 is the oldest). When two users have the same age they share a rank, and the next rank is skipped (1, 2, 2, 4), as in sports standings.

Write a query returning `name`, `region`, `age` and the rank as `age_rank`, using the `RANK()` window function.

### Constraints

- Columns, in order: `name`, `region`, `age`, `age_rank`
- Ranks restart in every region
- Ties share a rank and leave a gap afterwards

### Hints

<details>
<summary>Hint 1</summary>

`RANK() OVER (PARTITION BY ... ORDER BY ...)`

</details>

<details>
<summary>Hint 2</summary>

`PARTITION BY region` restarts the ranking per region; `ORDER BY age DESC` puts the oldest first.

</details>

## Theory

### The simple version

`RANK()` numbers rows from best to worst. Ties share a number and the next number is skipped, like a race.

### Window functions

A window function computes a value for each row using a _window_ of related rows, **without collapsing them** like `GROUP BY` does:

```sql
SELECT name, region, age,
       RANK() OVER (PARTITION BY region ORDER BY age DESC) AS age_rank
FROM users;
```

- `PARTITION BY region` splits the rows into independent groups.
- `ORDER BY age DESC` orders the rows inside each group.
- `RANK()` numbers them.

### How RANK treats ties

With ages 40, 35, 35, 28 in the same region the ranks are **1, 2, 2, 4**: both 35s share rank 2, and Diana gets rank 4 because three people are ahead of her. In other words, a row's rank is 1 plus the number of rows strictly ahead of it.

### Compared with GROUP BY

`GROUP BY` returns one row per group. A window function keeps every row and adds a column. That is why "top-N per group" and "rank within group" use window functions.

### Availability

Window functions need SQLite 3.25 or later; this editor runs 3.39.

## Explanation

`PARTITION BY region` ranks each region on its own. In the North, Bob and Charlie are both 35, so both get rank 2 and Diana gets 4. The hidden rows add a tie in the South and a new region.
