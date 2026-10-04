---
name: db-sql-in-list
title: 'IN List Matching'
tags: [db]
difficulty: Beginner
---

## Statement

Your permission system restricts actions for young users and seniors. You want to flag users in specific age groups (under 13, 13-17, over 65). Write a query that efficiently returns users in these age categories.

Write a query returning all columns from `users` where `age` is in the list (12, 16, 66).

### Constraints

- Return all columns
- Only rows where age is in the list 12, 16, or 66

### Hints

<details>
<summary>Hint 1</summary>

IN checks if a value matches any item in a list.

</details>

<details>
<summary>Hint 2</summary>

WHERE age IN (12, 16, 66) is equivalent to WHERE age = 12 OR age = 16 OR age = 66.

</details>

## Theory

### IN matches against a list of values

WHERE age IN (12, 16, 66) returns rows where age equals 12, 16, or 66.

### IN vs OR

These are equivalent:
- WHERE age IN (12, 16, 66)
- WHERE age = 12 OR age = 16 OR age = 66

IN is clearer and more efficient for many values.

### Why IN matters

- Membership checks: is this user in the allowed set?
- Bulk filtering: find rows matching multiple specific values
- Readability: shorter and clearer than chained OR conditions

## Explanation

The solution is SELECT * FROM users WHERE age IN (12, 16, 66);. The database returns rows where age matches any value in the list.
