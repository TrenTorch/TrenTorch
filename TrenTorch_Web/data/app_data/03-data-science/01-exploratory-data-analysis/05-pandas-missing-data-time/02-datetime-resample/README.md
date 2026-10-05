---
name: data-science-pandas-datetime-resample
title: Dates, Resampling & Rolling Windows
tags: [data-science, pandas, datetime, time-series]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Dates arrive as text: `"2024-03-07"`, sometimes `"03/07/24"`, sometimes a typo. Until they are turned into real timestamps they are just strings, you cannot subtract them, group them by month, or tell that March comes before April only because of the spelling. Once they are timestamps, a whole vocabulary opens up: pull out the year or the weekday, count the days between two events, total sales per month, smooth a noisy series with a moving average.

This question builds those five time-series tools: parsing with bad values handled, calendar features, a monthly total that does not skip empty months, a moving average, and a day count between two columns of dates.

### From theory to code

Implement `parse_dates(s)`, `calendar_features(dates)`, `monthly_total(df, date_col, value_col)`, `rolling_average(s, window)` and `days_between(start, end)`. The signatures and docstrings are already in the editor.

### Constraints

- `parse_dates(s)` converts text in the exact format `YYYY-MM-DD` to a datetime Series with `s`'s index. A value that is not a valid date in that format (a typo, `"2024-02-30"`, a missing value) becomes `NaT` instead of raising.
- `calendar_features(dates)` takes a datetime Series with **no missing values** and returns a frame with `dates`'s index and the integer columns `year`, `month` (1 to 12) and `dayofweek` (Monday = 0), plus the boolean column `is_weekend` (Saturday or Sunday), in that order.
- `monthly_total(df, date_col, value_col)` takes a frame whose `date_col` holds datetimes and returns a Series of the **sum of `value_col` per calendar month**, indexed by the first day of each month at midnight, covering every month from the earliest to the latest one **including months with no rows (total `0`)**. The Series is named `value_col`.
- `rolling_average(s, window)` returns the mean of each value and the `window - 1` before it. The first `window - 1` results are `NaN` (a window must be full). `s` is indexed by dates.
- `days_between(start, end)` takes two datetime Series with the same index (no missing values) and returns the whole number of days from `start` to `end` as an integer Series (negative if `end` is earlier).

### Hints

<details>
<summary>Hint 1</summary>

`pd.to_datetime` has `format` and `errors` arguments. One of the `errors` options turns failures into `NaT`.

</details>

<details>
<summary>Hint 2</summary>

The `.dt` accessor of a datetime Series has `year`, `month`, `dayofweek` and more.

</details>

<details>
<summary>Hint 3</summary>

`resample("MS")` groups a datetime-indexed Series into calendar months labelled by their first day, and creates the empty months too.

</details>

## Theory

### The simple version

A date written as text is a label on a drawer. A real timestamp is a position on a number line, which is what lets you ask "how far apart?", "which month?" and "what is the average of the last seven days?". Resampling is cutting that line into equal calendar slices (months, weeks) and adding up whatever fell inside each. A rolling window is a short ruler slid along the line, averaging whatever it covers.

### Parsing

`pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")` interprets text with an explicit format. Giving the format is faster and, more importantly, unambiguous: `"03/07/24"` is March 7th in one country and July 3rd in another. With `errors="coerce"` any value that does not fit becomes `NaT` ("not a time", the missing value for dates), so one bad row does not kill the whole load, and `isna()` then finds the rows to investigate.

### The `.dt` accessor

On a datetime Series, `s.dt.year`, `.month`, `.dayofweek`, `.day_name()`, `.floor("D")` and friends extract calendar parts. Weekday numbering is a classic trap: pandas counts Monday as 0 and Sunday as 6.

### Resampling

For a Series with a datetime index, `s.resample("MS").sum()` assigns each value to its month and aggregates. The alias `MS` means "month start", so the label of each bin is the first day of the month. Bins with no data are still created, giving `0` for a sum, which is what keeps a monthly chart honest about quiet months. (`"M"`/`"ME"` label by month end and changed spelling between pandas versions; `MS` is stable.)

### Rolling windows

$$
\text{ra}_t = \frac{1}{w}\sum_{k=0}^{w-1} x_{t-k}
$$

A rolling mean smooths noise at the price of lag, and the first $w-1$ values are `NaN` because the window is not yet full (`min_periods` can relax that). The window here is a _count of rows_; a window of time (such as `"7D"`) is a different, calendar-aware tool.

### Differences

Subtracting two datetime Series gives a _timedelta_ Series, and `.dt.days` is its whole-day part. For events 36 hours apart the answer is 1, not 1.5, because `days` truncates the fraction.

### How pandas actually implements this

Datetimes are stored as 64-bit integers (nanoseconds since 1970), so parsing is vectorised and comparisons and subtraction are integer operations. `resample` builds the bin edges from the index frequency and uses a `groupby` over them. `rolling` keeps a running window aggregate, so a rolling mean is $O(n)$ rather than $O(nw)$.

## Explanation

`parse_dates` calls `pd.to_datetime` with the explicit format and `errors="coerce"`, so anything unparseable becomes `NaT`. `calendar_features` reads `year`, `month` and `dayofweek` from the `.dt` accessor and derives `is_weekend` from weekday numbers 5 and 6. `monthly_total` sets the date column as the index and resamples with `"MS"` and a sum, which labels each month by its first day and includes empty months as `0`. `rolling_average` is `s.rolling(window).mean()`, whose first `window - 1` entries are `NaN`. `days_between` subtracts the Series and takes `.dt.days`, which truncates to whole days.
