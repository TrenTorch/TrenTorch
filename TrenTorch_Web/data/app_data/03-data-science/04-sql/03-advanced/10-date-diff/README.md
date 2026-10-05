---
name: db-sql-date-diff
title: 'Date Functions: Time Calculations'
tags: [db]
difficulty: Advanced
---

## Statement

Reports are produced "as of" a fixed date so they are reproducible: **2024-06-30**. For every user compute:

- `age_years`: the number of **completed** years between `birth_date` and 2024-06-30 (a birthday that has not happened yet this year does not count), and
- `days_registered`: the number of whole days between `registered_on` and 2024-06-30.

Dates are stored as `'YYYY-MM-DD'` text. Write a query returning `name`, `age_years` and `days_registered`.

### Constraints

- Columns, in order: `name`, `age_years`, `days_registered`
- Use the fixed reference date `'2024-06-30'`, not `'now'`
- Age counts completed years only (a birthday on 2024-06-30 itself counts as already happened)

### Hints

<details>
<summary>Hint 1</summary>

`julianday(date)` converts a date to a day number, so subtracting two of them gives days.

</details>

<details>
<summary>Hint 2</summary>

Years: subtract the years, then subtract 1 if the month-day of the birthday is still ahead of 2024-06-30.

</details>

## Theory

### The simple version

SQLite stores dates as text. Functions like `julianday` turn them into numbers so you can subtract them to get days.

### Dates in SQLite

SQLite has no dedicated date type. Dates are stored as text (`'2024-06-30'`), numbers or Julian days, and the date functions interpret them:

```sql
SELECT date('2024-06-30', '+7 days');          -- 2024-07-07
SELECT strftime('%Y', '2024-06-30');           -- '2024'
SELECT julianday('2024-06-30') - julianday('2024-01-01');   -- 181.0
```

### Differences in days

`julianday(a) - julianday(b)` is the number of days (with a fraction if times are included). Wrap it in `CAST(... AS INTEGER)` for whole days.

### Age in completed years

Years cannot be found by dividing days by 365: leap years make it drift. Compare the calendar parts instead:

```sql
year(now) - year(birth) - (monthday(now) < monthday(birth))
```

In SQLite, `strftime('%m-%d', date)` gives the month-day text, and comparing two `'MM-DD'` strings alphabetically works because the format is zero-padded. A comparison returns 1 or 0, so it can be subtracted directly.

### Avoid 'now' in tests and reports

`date('now')` changes every day, so a result can never be compared with a fixed expectation. Use an explicit "as of" date, which also makes reports reproducible.

## Explanation

Alice (born 1990-03-15) has had her 2024 birthday, so she is 34; Bob (2000-12-31) has not, so he is 23; Charlie's birthday is exactly 06-30, which counts as reached, so 39. Days registered use `julianday`. The hidden data covers a person born on 1 January and a registration on a leap day.
