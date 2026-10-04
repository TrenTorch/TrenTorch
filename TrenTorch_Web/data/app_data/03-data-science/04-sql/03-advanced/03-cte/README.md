---
name: db-sql-cte
title: Common Table Expressions
tags: ["db"]
difficulty: Advanced
---

## Statement
WITH high_earners AS (SELECT * FROM employees WHERE salary > 100000) SELECT * FROM high_earners

Write a solution that solves this problem efficiently.

## Theory
Understand the underlying principles behind this problem. Think about time complexity, space complexity, and edge cases.

Consider:
- What is the simplest correct solution?
- Can you optimize further?
- What are the constraints?

## Explanation
The key to solving this problem is balancing correctness with efficiency. Start with a working solution, then profile and optimize based on actual bottlenecks.

