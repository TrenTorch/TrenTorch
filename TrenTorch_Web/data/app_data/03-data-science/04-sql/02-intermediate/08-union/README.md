---
name: db-sql-union
title: 'UNION Combining Queries'
tags: [db]
difficulty: Intermediate
---

## Statement

Your reporting combines two separate data sources. Combine active users and archived users into one result set using UNION.

Write a query that returns all users from the users table UNION all users from an archive_users table.

## Theory

UNION combines results from two SELECT queries into one and removes duplicates. UNION ALL keeps all rows.

## Explanation

The solution uses UNION to combine users from two tables with automatic deduplication.
