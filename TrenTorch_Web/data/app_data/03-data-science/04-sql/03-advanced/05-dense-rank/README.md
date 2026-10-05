---
name: db-sql-dense-rank
title: 'DENSE_RANK: Window Function without Gaps'
tags: [db]
difficulty: Advanced
---

## Statement

A quiz leaderboard awards medal levels: highest score is level 1, and people with the same score share a level. Unlike sports standings there should be **no gaps**: after two people tie for level 2 the next score is level 3, not 4.

Write a query returning `name`, `score` and the level as `score_rank`, using `DENSE_RANK()`.

### Constraints

- Columns, in order: `name`, `score`, `score_rank`
- Highest score has `score_rank` 1
- Ties share a rank and the next rank follows immediately (1, 2, 2, 3)

### Hints

<details>
<summary>Hint 1</summary>

`DENSE_RANK() OVER (ORDER BY score DESC)`

</details>

<details>
<summary>Hint 2</summary>

`RANK()` would leave a gap after a tie; `DENSE_RANK()` does not.

</details>

## Theory

### The simple version

`DENSE_RANK()` also shares a number for ties, but the next number follows straight on: 1, 2, 2, 3.

### Ranking without gaps

```sql
SELECT name, score,
       DENSE_RANK() OVER (ORDER BY score DESC) AS score_rank
FROM scores;
```

`DENSE_RANK` numbers distinct values: 95 → 1, 90 → 2 (for both people), 85 → 3, 70 → 4.

### RANK vs DENSE_RANK vs ROW_NUMBER

| Scores         | 95  | 90  | 90  | 85  |
| -------------- | --- | --- | --- | --- |
| `ROW_NUMBER()` | 1   | 2   | 3   | 4   |
| `RANK()`       | 1   | 2   | 2   | 4   |
| `DENSE_RANK()` | 1   | 2   | 2   | 3   |

### When to use it

Pick `DENSE_RANK` for "levels" and "N-th highest value": `WHERE score_rank = 2` returns everyone with the second-highest _distinct_ score, even if several people share it.

### Filtering on a window result

You cannot use a window function in `WHERE` directly. Wrap the query in a subquery or CTE and filter the outer query.

## Explanation

Scores 95, 90, 90, 85, 70 receive levels 1, 2, 2, 3, 4. The hidden dataset ties two people at 95, shifting every level, which checks the ordering and the no-gap behaviour at once.
