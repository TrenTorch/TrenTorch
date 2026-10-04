---
name: db-sql-self-join
title: Self-Join (Employee-Manager)
tags: ["db"]
difficulty: Intermediate
---

## Statement
SELECT e.name, m.name FROM employees e LEFT JOIN employees m ON e.manager_id = m.id

Write a solution that solves this problem efficiently.

## Theory
Understand the underlying principles behind this problem. Think about time complexity, space complexity, and edge cases.

Consider:
- What is the simplest correct solution?
- Can you optimize further?
- What are the constraints?

## Explanation
The key to solving this problem is balancing correctness with efficiency. Start with a working solution, then profile and optimize based on actual bottlenecks.

