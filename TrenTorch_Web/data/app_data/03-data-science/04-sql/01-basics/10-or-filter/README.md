---
name: db-sql-or-filter
title: 'OR Alternative Filtering'
tags: [db]
difficulty: Beginner
---

## Statement

Age-appropriate messaging applies to very young users (under 18) and to seniors (over 65). A user matching **either** condition should be included.

Write a query returning all columns of `users` where `age < 18` OR `age > 65`.

### Constraints

- Return all columns
- Include a row if at least one condition holds
- 18 and 65 themselves are not included

### Hints

<details>
<summary>Hint 1</summary>

Combine the two conditions with `OR`.

</details>

<details>
<summary>Hint 2</summary>

Repeat the column name in each comparison: `age < 18 OR age > 65`.

</details>

## Theory

### The simple version

`OR` means a row is kept if at least one of the conditions is true.

### OR: at least one condition

```sql
SELECT * FROM users WHERE age < 18 OR age > 65;
```

`OR` keeps a row when **either** side is true. It widens the result, the opposite of `AND`.

### A classic mistake

`WHERE age < 18 AND age > 65` returns nothing, because no number is both below 18 and above 65. When you mean "outside a range" you want `OR`; when you mean "inside a range" you want `AND` (or `BETWEEN`).

### Mixing with AND

`AND` is evaluated before `OR`. `a OR b AND c` means `a OR (b AND c)`. Use parentheses whenever both appear.

### Many equality tests

`WHERE age = 12 OR age = 16 OR age = 66` is better written as `age IN (12, 16, 66)`, which is covered in a later question.

## Explanation

`age < 18 OR age > 65` keeps users outside the 18-65 band. The boundary users aged 18 and 65 are deliberately in the data: a query using `<=` or `>=` would include them and the row comparison would fail.
