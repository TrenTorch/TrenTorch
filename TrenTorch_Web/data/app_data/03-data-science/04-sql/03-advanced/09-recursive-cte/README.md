---
name: db-sql-recursive-cte
title: 'Recursive CTE: Hierarchical Data'
tags: [db]
difficulty: Advanced
---

## Statement

Navigate an org chart: find all employees under a manager (manager → direct reports → their reports, recursively). Use recursive CTE to traverse the hierarchy.

## Theory

### Recursive CTEs traverse hierarchies

A recursive CTE calls itself, enabling traversal of tree or graph structures:

WITH RECURSIVE org_hierarchy AS (
  SELECT id, name, manager_id, 1 as level FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, oh.level + 1 FROM employees e JOIN org_hierarchy oh ON e.manager_id = oh.id
) SELECT * FROM org_hierarchy;

Base case: Find root nodes (employees with no manager).
Recursive case: Find children of already-found nodes.

### Recursive CTE structure

1. Base case: initial rows (roots)
2. UNION ALL: combines base with recursive results
3. Recursive case: references the CTE itself to expand

### Use cases

- Org hierarchies: manager → direct reports → their reports
- Category trees: parent → children → grandchildren
- Paths and networks: graph traversal
- Genealogy: ancestors or descendants

### Termination

Recursion stops when the recursive case produces no new rows.

## Explanation

The solution uses a recursive CTE to build an organization hierarchy, starting from employees with no manager, then recursively adding their direct and indirect reports.
