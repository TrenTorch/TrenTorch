---
name: db-sql-or-filter
title: 'OR Alternative Filtering'
tags: [db]
difficulty: Beginner
---

## Statement

Your notification system needs to alert users who are either very young (under 18) or very old (over 65) for age-appropriate messaging. Write a query that returns users matching at least one of these criteria.

Write a query returning all columns from `users` where `age < 18` OR `age > 65`.

### Constraints

- Return all columns
- age < 18 OR age > 65

### Hints

<details>
<summary>Hint 1</summary>

The OR operator combines conditions; at least one must be true.

</details>

<details>
<summary>Hint 2</summary>

Rows satisfying either condition (or both) are included.

</details>

## Theory

### OR requires at least one condition to be true

WHERE age < 18 OR age > 65 returns rows where at least one condition holds. A row satisfying both conditions is also included.

### Combining AND and OR

WHERE age >= 18 AND (name LIKE 'A%' OR email LIKE '%gmail%') uses parentheses to control which conditions group together.

### Truth table for OR

- TRUE OR TRUE = TRUE
- TRUE OR FALSE = TRUE
- FALSE OR TRUE = TRUE
- FALSE OR FALSE = FALSE

## Explanation

The solution is SELECT * FROM users WHERE age < 18 OR age > 65;. The database returns rows where the age falls outside the 18-65 range.
