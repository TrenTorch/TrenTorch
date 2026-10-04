---
name: db-sql-nth-highest
title: 'NTH Highest Value'
tags: [db]
difficulty: Intermediate
---

## Statement

Your analytics needs the second-highest user age. Use a subquery or sorting technique to find the nth highest value without aggregation.

Write a query returning the second-highest age in the users table.

### Constraints

- Return a single value: the second-highest age

### Hints

<details>
<summary>Hint 1</summary>

ORDER BY DESC and LIMIT 1 OFFSET 1 skips the first (highest) and returns the second.

</details>

<details>
<summary>Hint 2</summary>

OFFSET skips rows; OFFSET 1 skips the first row.

</details>

## Theory

### Finding the nth highest value

LIMIT 1 OFFSET 1 returns the second row when ordered descending:

```sql
SELECT DISTINCT age FROM users ORDER BY age DESC LIMIT 1 OFFSET 1;
```

DISTINCT handles duplicates; OFFSET skips the first (highest) value.

## Explanation

The solution orders ages descending, uses OFFSET to skip the highest, and LIMIT to return one row (the second-highest).
