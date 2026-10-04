---
name: db-sql-dense-rank
title: DENSE_RANK()
tags: ["db"]
difficulty: Advanced
---

## Statement
SELECT name, RANK() OVER (PARTITION BY department ORDER BY salary DESC) FROM employees

Write a solution that solves this problem efficiently.

## Theory
Understand the underlying principles behind this problem. Think about time complexity, space complexity, and edge cases.

Consider:
- What is the simplest correct solution?
- Can you optimize further?
- What are the constraints?

## Explanation
The key to solving this problem is balancing correctness with efficiency. Start with a working solution, then profile and optimize based on actual bottlenecks.

