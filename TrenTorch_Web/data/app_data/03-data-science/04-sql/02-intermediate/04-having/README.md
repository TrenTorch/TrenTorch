---
name: db-sql-having
title: 'HAVING Filtering Groups'
tags: [db]
difficulty: Intermediate
---

## Statement

Marketing wants repeat customers only: users who placed **more than one** order.

Write a query returning `user_id` and `order_count` for the users that have more than 1 order, using `GROUP BY` and `HAVING`.

### Constraints

- Columns, in order: `user_id`, `order_count`
- Only groups whose count is greater than 1

### Hints

<details>
<summary>Hint 1</summary>

`WHERE` cannot see aggregate results; `HAVING` can.

</details>

<details>
<summary>Hint 2</summary>

`HAVING COUNT(*) > 1` goes right after `GROUP BY`.

</details>

## Theory

### The simple version

`HAVING` filters the piles created by `GROUP BY`, the same way `WHERE` filters individual rows.

### Filtering groups with HAVING

```sql
SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 1;
```

`HAVING` is `WHERE` for groups: it runs **after** grouping, so it can use aggregates.

### WHERE vs HAVING

|                    | WHERE             | HAVING           |
| ------------------ | ----------------- | ---------------- |
| Filters            | individual rows   | whole groups     |
| Runs               | before `GROUP BY` | after `GROUP BY` |
| Can use aggregates | no                | yes              |

`WHERE COUNT(*) > 1` is an error in SQLite: _misuse of aggregate_.

### Use WHERE when you can

A condition on a plain column (`WHERE amount > 100`) should go in `WHERE`: it discards rows before grouping and does less work. Reserve `HAVING` for conditions on aggregates.

### Aliases

SQLite lets you write `HAVING order_count > 1` using the alias, but other databases do not, so repeating the aggregate is more portable.

## Explanation

Grouping gives user 1 two orders, user 2 one order and user 3 three orders; `HAVING COUNT(*) > 1` keeps users 1 and 3. Putting the condition in `WHERE` fails with _misuse of aggregate_.
