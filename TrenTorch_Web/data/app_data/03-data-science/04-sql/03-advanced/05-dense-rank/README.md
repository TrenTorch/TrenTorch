---
name: db-sql-dense-rank
title: 'DENSE_RANK: Window Function without Gaps'
tags: [db]
difficulty: Advanced
---

## Statement

Rank users by score, ensuring consecutive ranks even when ties exist (1, 2, 2, 3, not 1, 2, 2, 4).

## Theory

### DENSE_RANK avoids rank gaps

DENSE_RANK() is like RANK() but without gaps in the rank sequence:

SELECT name, score, DENSE_RANK() OVER (ORDER BY score DESC) as rank FROM users;

Two users with the same score get the same rank; the next rank is consecutive, not skipped.

### RANK vs DENSE_RANK

- RANK(): 1, 2, 2, 4 (gap after tie)
- DENSE_RANK(): 1, 2, 2, 3 (no gap)

Use DENSE_RANK when you want consecutive rankings (e.g., medals: gold, silver, bronze, no tie-skip).

### Practical use cases

- Leaderboards with ties (multiple gold medalists)
- Percentile ranking without gaps
- Categorical grouping based on rank

## Explanation

The solution uses DENSE_RANK() OVER (ORDER BY score DESC) to rank users, ensuring consecutive ranks even when multiple users share the same score.
