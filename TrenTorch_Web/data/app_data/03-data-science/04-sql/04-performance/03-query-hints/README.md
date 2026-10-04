---
name: db-sql-perf-query-hints
title: 'Query Hints'
tags: [db]
difficulty: Advanced
---

## Statement

Force execution plans with optimizer hints. Understand how databases optimize execution and improve query performance.

### Key concepts
- Database query optimization
- Cost-based planning
- Resource constraints and trade-offs

### Hints

<details>
<summary>Hint 1</summary>

Think about how the database chooses between different execution strategies.

</details>

<details>
<summary>Hint 2</summary>

What information does the optimizer need to make good decisions?

</details>

## Theory

### Core Principle

Query optimization is about choosing the cheapest execution plan. The optimizer estimates cost using:
- Table cardinality (row counts)
- Column statistics (value distribution)
- Index availability
- Join selectivity

### Why Performance Matters

- Slow queries block entire systems
- Bad plans compound at scale (1000x cost difference)
- Production incidents often trace to query regression
- Monitoring and tuning are critical operational skills

### Trade-offs

- Index creation costs write performance
- Materialized views consume storage
- Caching adds staleness risk
- Parallelism has overhead

## Explanation

The solution identifies the bottleneck using EXPLAIN, gathers stats, and applies the appropriate optimization. Key: measure before and after to confirm improvement.

