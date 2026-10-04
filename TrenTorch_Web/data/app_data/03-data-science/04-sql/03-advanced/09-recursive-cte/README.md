---
name: db-sql-recursive-cte
title: Recursive CTEs
tags: ["db"]
difficulty: Advanced
---

## Statement
WITH RECURSIVE nums(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM nums WHERE n < 10) SELECT * FROM nums

Write a solution that solves this problem efficiently.

## Theory
Understand the underlying principles behind this problem. Think about time complexity, space complexity, and edge cases.

Consider:
- What is the simplest correct solution?
- Can you optimize further?
- What are the constraints?

## Explanation
The key to solving this problem is balancing correctness with efficiency. Start with a working solution, then profile and optimize based on actual bottlenecks.

