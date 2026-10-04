---
name: db-sql-rank
title: 'RANK: Window Function with Gaps'
tags: [db]
difficulty: Advanced
---

## Statement

Rank users by age within their region. If two users have the same age, they share the same rank, and the next rank skips (e.g., 1, 2, 2, 4, not 1, 2, 2, 3).

## Theory

### Window functions compute per-row without collapsing

RANK() is a window function that assigns a rank to each row within a partition:

SELECT region, name, age, RANK() OVER (PARTITION BY region ORDER BY age DESC) as rank FROM users;

For each region, this ranks users by age (descending). Ties get the same rank; the next rank accounts for ties.

### RANK vs other window functions

- RANK(): same rank for ties, next rank skips (1, 2, 2, 4)
- DENSE_RANK(): same rank for ties, next rank consecutive (1, 2, 2, 3)
- ROW_NUMBER(): unique rank per row, no ties (1, 2, 3, 4)

### Window function anatomy

OVER (...) defines the window:
- PARTITION BY: group rows (compute per group)
- ORDER BY: sort within each partition

### Why window functions matter

- Ranking and leaderboards
- Running totals and moving averages
- Accessing previous/next rows (LAG/LEAD)
- Comparison within groups without collapsing rows

## Explanation

The solution uses RANK() OVER (PARTITION BY region ORDER BY age DESC) to rank users within each region by age, with ties sharing a rank and subsequent ranks skipping numbers.
