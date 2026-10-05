---
name: db-sql-like
title: 'LIKE Pattern Matching'
tags: [db]
difficulty: Beginner
---

## Statement

Your search feature lets support staff find users by email domain. Return everyone whose email address ends with `@example.com`. Addresses such as `carol@example.com.au` (a different domain) and `erin@notexample.com` must not be matched. SQLite's `LIKE` ignores case for ASCII letters, so `dave@EXAMPLE.COM` does count.

Write a query returning all columns of `users` whose `email` ends with `'@example.com'`.

### Constraints

- Return all columns
- The address must **end** with `@example.com`
- Match case-insensitively (the default for SQLite's `LIKE`)

### Hints

<details>
<summary>Hint 1</summary>

`%` in a `LIKE` pattern means "any characters".

</details>

<details>
<summary>Hint 2</summary>

Put the `%` at the start of the pattern so only the ending is fixed.

</details>

## Theory

### The simple version

`LIKE` matches text against a pattern, where `%` stands for "any characters".

### Wildcards

```sql
SELECT * FROM users WHERE email LIKE '%@example.com';
```

`LIKE` compares text with a pattern. `%` matches any sequence of characters (including none); `_` matches exactly one character.

| Pattern  | Meaning            |
| -------- | ------------------ |
| `'A%'`   | starts with A      |
| `'%son'` | ends with son      |
| `'%li%'` | contains li        |
| `'_o%'`  | second letter is o |

### Anchoring matters

Without a leading `%` the pattern must match from the first character; without a trailing `%` it must match to the last. Including the `@` in the pattern is what prevents `notexample.com` from matching.

### Case and performance

In SQLite, `LIKE` is case-insensitive for ASCII; `GLOB` is the case-sensitive alternative. A pattern that starts with `%` cannot use an ordinary index, so it scans the whole column.

### Literal % and _

To match a real percent sign use `ESCAPE`: `LIKE '50\%%' ESCAPE '\'`.

## Explanation

`LIKE '%@example.com'` fixes the end of the string and allows anything before it. The data includes near-misses on purpose: a longer domain (`.com.au`), a different domain that merely contains the text (`notexample.com`), and an upper-case address that should match.
