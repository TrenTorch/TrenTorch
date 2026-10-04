---
name: db-sql-having
title: HAVING Clause
tags: ["db"]
difficulty: Intermediate
---

## Statement
SELECT department, COUNT(*) as cnt FROM users GROUP BY department HAVING COUNT(*) > 1

Write a solution that solves this problem efficiently.

## Theory
Understand the underlying principles behind this problem. Think about time complexity, space complexity, and edge cases.

Consider:
- What is the simplest correct solution?
- Can you optimize further?
- What are the constraints?

## Explanation
The key to solving this problem is balancing correctness with efficiency. Start with a working solution, then profile and optimize based on actual bottlenecks.

