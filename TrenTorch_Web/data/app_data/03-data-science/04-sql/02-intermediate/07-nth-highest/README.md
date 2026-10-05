---
name: db-sql-nth-highest
title: 'NTH Highest Value'
tags: [db]
difficulty: Intermediate
---

## Statement

Analytics needs the **second-highest age** among users. Two users are tied for the highest age (40), and the tie must count as one level: the answer is the next _different_ age. One user has no age recorded.

Write a query that returns a single value: the second-highest distinct `age`.

### Constraints

- Return a single row with a single column
- Ties count once (use distinct ages)
- Ignore users whose age is NULL

### Hints

<details>
<summary>Hint 1</summary>

Sort distinct ages descending and skip the first one.

</details>

<details>
<summary>Hint 2</summary>

`LIMIT 1 OFFSET 1` returns the second row.

</details>

## Theory

### The simple version

Sort the distinct values from largest down, skip the first ones you do not want, and take the next one.

### The N-th highest value

Sort the distinct values from high to low, skip `N - 1` of them, and take one:

```sql
SELECT DISTINCT age
FROM users
WHERE age IS NOT NULL
ORDER BY age DESC
LIMIT 1 OFFSET 1;      -- 2nd highest; use OFFSET 2 for the 3rd
```

### Why DISTINCT

Without it, two users aged 40 occupy positions 1 and 2, so "second highest" would wrongly return 40. `DISTINCT` collapses ties first.

### Why exclude NULL

In SQLite, `NULL` sorts as the smallest value, so in descending order it comes last and would only matter for tiny tables, but filtering it explicitly keeps the intent obvious and is safe in other databases where NULL may sort first.

### If there is no N-th value

When fewer than N distinct values exist the query returns **no rows** (not NULL). Wrap it as a scalar subquery if you need NULL: `SELECT (SELECT DISTINCT ...)`.

### Alternative: window functions

`DENSE_RANK() OVER (ORDER BY age DESC)` numbers distinct levels directly, which generalises to "N-th highest per department".

## Explanation

Distinct ages sorted descending are 40, 30, 25, so `OFFSET 1` lands on 30. Without `DISTINCT` the duplicate 40 would be returned. A second dataset with two users aged 55 changes the answer to 40, so the value must be computed.
