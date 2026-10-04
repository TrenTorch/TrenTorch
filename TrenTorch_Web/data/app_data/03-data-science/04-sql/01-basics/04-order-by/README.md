---
name: db-sql-order-by
title: 'ORDER BY Sorting'
tags: [db]
difficulty: Beginner
---

## Statement

Your application displays a leaderboard of users sorted by age (oldest first). The users table contains data in arbitrary order; you need to organize it for display.

Write a query that returns all columns from the `users` table, sorted by `age` in descending order (highest age first).

### Constraints

- Return all columns
- Sort by age, highest age first (descending)

### Hints

<details>
<summary>Hint 1</summary>

The ORDER BY clause sorts results. Use DESC for descending (highest to lowest).

</details>

<details>
<summary>Hint 2</summary>

Without DESC, ORDER BY sorts ascending by default.

</details>

## Theory

### The ORDER BY clause sorts rows

While WHERE filters which rows appear, ORDER BY controls their sequence in the result. ASC (ascending) goes from lowest to highest; DESC (descending) goes from highest to lowest.

### Multi-column sorting

You can sort by multiple columns: ORDER BY age DESC, name ASC sorts by age descending, then by name ascending for users with the same age.

### Why sorting matters

- Leaderboards: rank users by score
- Reports: group similar items together
- User interfaces: alphabetical lists, reverse-chronological timestamps
- Business logic: process high-priority items first

## Explanation

The solution is SELECT * FROM users ORDER BY age DESC;. The database returns every row and column, but arranges them so the user with the highest age appears first, descending to the lowest.
