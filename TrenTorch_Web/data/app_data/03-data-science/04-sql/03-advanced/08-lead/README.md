---
name: db-sql-lead
title: 'LEAD: Access Next Row'
tags: [db]
difficulty: Advanced
---

## Statement

A retention analysis asks: after each event, what did the same user do next? Each user's events form their own timeline ordered by `ts`; the last event of a timeline has no next event.

Write a query returning `user_id`, `event` and the following event of the same user as `next_event`, using `LEAD()`.

### Constraints

- Columns, in order: `user_id`, `event`, `next_event`
- Only look at the same user's events (partition by user)
- The last event of each user has `next_event` NULL

### Hints

<details>
<summary>Hint 1</summary>

`LEAD` is the mirror image of `LAG`: it reads the next row.

</details>

<details>
<summary>Hint 2</summary>

Use `PARTITION BY user_id ORDER BY ts` so users do not mix.

</details>

## Theory

### The simple version

`LEAD` lets a row look at the row after it, which is how you ask "what happened next?".

### Looking at the next row

```sql
SELECT user_id, event,
       LEAD(event) OVER (PARTITION BY user_id ORDER BY ts) AS next_event
FROM events;
```

`LEAD(x)` returns `x` from the **next** row in the window; the last row gets `NULL`. It is the counterpart of `LAG`.

### Why PARTITION BY

Without it, the window is the whole table, so the last event of user 1 would see the _first_ event of user 2 as its "next" one. `PARTITION BY user_id` gives every user an independent timeline.

### Typical uses

- Funnel analysis (what happens after signup?).
- Time to next event: `julianday(LEAD(ts) OVER (...)) - julianday(ts)`.
- Detecting gaps in sequences.

### Offsets and defaults

`LEAD(x, 2)` looks two rows ahead and `LEAD(x, 1, 'none')` replaces the missing value with a default.

## Explanation

Within each user's timeline `LEAD(event)` returns the next event: user 1 goes signup → login → purchase → NULL. Without the partition, user 1's last event would wrongly point at user 2's signup.
