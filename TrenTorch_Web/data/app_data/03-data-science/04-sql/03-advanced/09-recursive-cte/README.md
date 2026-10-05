---
name: db-sql-recursive-cte
title: 'Recursive CTE: Hierarchical Data'
tags: [db]
difficulty: Advanced
---

## Statement

`employees.manager_id` points to the manager's `id`. Alice (id 1) is at the top of one reporting tree; Gina (id 7) heads a different one.

Write a recursive CTE that returns `id`, `name` and `depth` of everyone below Alice: her direct reports have depth 1, their reports depth 2, and so on. Do not include Alice herself or anyone from Gina's tree.

### Constraints

- Columns, in order: `id`, `name`, `depth`
- Direct reports of id 1 have depth 1; each further level adds 1
- Use `WITH RECURSIVE`

### Hints

<details>
<summary>Hint 1</summary>

A recursive CTE has an anchor query, `UNION ALL`, and a recursive query that joins back to the CTE.

</details>

<details>
<summary>Hint 2</summary>

The anchor is Alice's direct reports; the recursive step finds employees whose `manager_id` is already in the CTE.

</details>

## Theory

### The simple version

A recursive CTE starts from some rows and keeps adding the rows connected to them until there are no more. It walks a hierarchy.

### Queries that call themselves

```sql
WITH RECURSIVE reports(id, name, depth) AS (
  SELECT id, name, 1 FROM employees WHERE manager_id = 1   -- anchor
  UNION ALL
  SELECT e.id, e.name, r.depth + 1                          -- recursive step
  FROM employees e
  JOIN reports r ON e.manager_id = r.id
)
SELECT id, name, depth FROM reports;
```

### How it runs

1. The **anchor** query runs once and produces the starting rows (depth 1).
2. The **recursive step** runs on the rows produced by the previous round, producing the next level.
3. It repeats until a round produces no new rows, then all rounds are combined.

### Guarding against infinite loops

If the data contains a cycle (A manages B, B manages A) the recursion never ends. Protect against it with a `depth` limit (`WHERE r.depth < 10`) or use `UNION` instead of `UNION ALL` so repeated rows stop the recursion. This editor stops any statement that runs for more than 5 seconds.

### Other uses

Generating number or date series, bill-of-materials explosion, finding all ancestors of a node, and graph traversal.

## Explanation

The anchor returns Bob and Charlie (depth 1). Each round then joins employees whose manager is already found: Diana and Frank (depth 2), then Eve (depth 3). Gina's tree is never reached because it does not start from Alice. The hidden data extends the tree one level deeper.
