---
name: db-sql-self-join
title: 'SELF JOIN'
tags: [db]
difficulty: Intermediate
---

## Statement

Your employee table has manager_id field pointing to another employee. Find all pairs (employee, manager) where the employee's manager_id matches another employee's id in the same table.

Write a query joining employees to their managers, returning employee name and manager name.

### Constraints

- Join employees table to itself
- Match employee manager_id to manager id

### Hints

<details>
<summary>Hint 1</summary>

Use table aliases (AS) to distinguish the same table in different roles.

</details>

<details>
<summary>Hint 2</summary>

FROM employees e1 JOIN employees e2 ON e1.manager_id = e2.id treats employees as both "employee" and "manager."

</details>

## Theory

### SELF JOIN connects a table to itself

When data references itself (like manager_id pointing to another employee's id), use a self join with different aliases:

```sql
SELECT e.name, m.name FROM employees e JOIN employees m ON e.manager_id = m.id;
```

Here, e is the employee and m is their manager, both from the same table.

## Explanation

The solution aliases the same table twice: once for employees, once for managers. The join condition matches employee manager_id to manager id.
