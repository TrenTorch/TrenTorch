---
name: db-sql-row-number
title: 'ROW_NUMBER: Unique Sequential Numbering'
tags: [db]
difficulty: Advanced
---

## Statement

Implement pagination: assign each user a unique sequential number (1, 2, 3, ...) ordered by age. Use ROW_NUMBER() to enable 'page 1: rows 1-10, page 2: rows 11-20' logic.

## Theory

### ROW_NUMBER assigns unique sequential numbers

ROW_NUMBER() assigns a unique number to each row within a partition, with no ties:

SELECT name, age, ROW_NUMBER() OVER (ORDER BY age DESC) as row_num FROM users;

Even if two users have identical ages, they get consecutive row numbers (no shared ranks).

### ROW_NUMBER vs RANK vs DENSE_RANK

- ROW_NUMBER(): 1, 2, 3, 4 (always unique, no ties)
- RANK(): 1, 2, 2, 4 (ties share rank, next skips)
- DENSE_RANK(): 1, 2, 2, 3 (ties share rank, next consecutive)

### Pagination with ROW_NUMBER

SELECT * FROM (SELECT *, ROW_NUMBER() OVER (ORDER BY created_at DESC) as rn FROM orders) WHERE rn BETWEEN 11 AND 20;

This returns rows 11-20 (page 2 with page size 10), essential for paginated APIs.

### Practical use cases

- Pagination (fetch rows N to M)
- Session numbering (divide data into chunks)
- De-duplication (select first occurrence per group)

## Explanation

The solution uses ROW_NUMBER() OVER (ORDER BY age DESC) to assign unique sequential numbers, enabling pagination by filtering on the row number range.
