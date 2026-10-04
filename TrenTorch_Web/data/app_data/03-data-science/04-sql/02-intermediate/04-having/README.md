---
name: db-sql-having
title: 'HAVING Filtering Groups'
tags: [db]
difficulty: Intermediate
---

## Statement

Your analytics shows order counts per user. You only want to report on users with more than 1 order (to exclude one-time buyers). Use HAVING to filter groups after aggregation.

Write a query returning `user_id` and order count for users with more than 1 order.

### Constraints

- Return user_id and order count
- Only groups (users) with count > 1

### Hints

<details>
<summary>Hint 1</summary>

WHERE filters rows before grouping; HAVING filters groups after aggregation.

</details>

<details>
<summary>Hint 2</summary>

HAVING applies to aggregate functions like COUNT, not to raw columns.

</details>

## Theory

### HAVING filters groups after aggregation

WHERE filters rows before grouping. HAVING filters the grouped results:

```sql
SELECT user_id, COUNT(*) FROM orders GROUP BY user_id HAVING COUNT(*) > 1;
```

This groups by user_id, counts orders per group, then filters to include only groups with count > 1.

### WHERE vs HAVING

- WHERE: filters rows before aggregation
- HAVING: filters groups after aggregation

## Explanation

The solution groups orders by user_id, counts per group, and uses HAVING to include only groups where the count exceeds 1.
