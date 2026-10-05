---
name: data-science-pandas-assemble-monthly-report
title: Assemble: A Monthly Sales Report
tags: [data-science, pandas, eda, assemble]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

This is the question the previous ones were building towards, and it is the shape of a thousand real tasks: raw order lines arrive as text, customers live in another table, and someone wants **one tidy table per month**: how many orders, how much revenue, the average order, how revenue moved against the month before, and which region sold the most. No single pandas call produces that. It needs parsing, a join, a group-by on a derived key, a calendar with no gaps, a shifted comparison, and a rule for ties.

Each of those steps is something you have already built. The point of the question is combining them without losing rows silently, and with every edge defined: bad dates, orders for unknown customers, empty months.

### From theory to code

Implement `monthly_report(orders, customers)`. The signature and docstring are already in the editor.

### Constraints

- `orders` has `order_id`, `customer_id`, `order_date` (text `YYYY-MM-DD`, possibly invalid) and `amount` (a number). `customers` has `id` (unique) and `region`.
- Ignore (do not count anywhere) orders whose `order_date` is not a valid `YYYY-MM-DD` date, and orders whose `customer_id` is not in `customers`.
- The result is indexed by **month start** (first day of the month, midnight), named `month`, covering **every month** from the earliest to the latest valid order, including months with no orders.
- Columns, in this order: `orders` (integer count), `revenue` (float sum of `amount`, `0.0` for an empty month), `avg_order_value` (`revenue / orders`, `NaN` when there are no orders), `growth_pct` (`100 * (revenue - previous month's revenue) / previous month's revenue`, `NaN` for the first month or when the previous month's revenue is `0`), `top_region` (the region with the highest revenue that month; ties go to the alphabetically smaller region; `None` or `NaN` for an empty month).
- If there is no valid order at all, return an empty frame with those five columns.
- The input frames are not changed.

### Hints

<details>
<summary>Hint 1</summary>

Build the pieces in order: parse the dates and drop the invalid ones, join the region, derive a month-start column, then aggregate.

</details>

<details>
<summary>Hint 2</summary>

`reindex` to a `pd.date_range(first, last, freq="MS")` creates the empty months, and `shift(1)` aligns each month with the one before it.

</details>

<details>
<summary>Hint 3</summary>

For `top_region`: sum revenue per (month, region), sort by month, revenue descending, region ascending, and keep the first row per month.

</details>

## Theory

### The simple version

A shop owner has a shoebox of receipts and wants a one-page monthly summary. You sort the receipts by month, throw out the unreadable ones, look up each customer's region in a notebook, then for each month write: how many receipts, the total, the average, whether it beat last month, and which region spent the most. The skill is doing those steps in an order where nothing is lost by accident.

### Pipeline thinking

| Step                  | Tool                                    | What can go wrong                                         |
| --------------------- | --------------------------------------- | --------------------------------------------------------- |
| parse dates           | `to_datetime(..., errors="coerce")`     | invalid dates become `NaT`: count or drop them on purpose |
| attach region         | `merge(..., how="inner")`               | unknown customers vanish; a duplicated id multiplies rows |
| month key             | `dt.to_period("M")` or `resample("MS")` | month-end vs month-start labels                           |
| aggregate             | `groupby("month").agg(...)`             | months with no rows are _absent_, not zero                |
| fill the calendar     | `reindex(date_range(..., freq="MS"))`   | introduces `NaN` that you must convert deliberately       |
| compare to last month | `shift(1)`                              | the first month has no predecessor                        |

### Derived measures

$$
\text{avg}_m = \frac{\text{revenue}_m}{\text{orders}_m}, \qquad
\text{growth}_m = 100\cdot\frac{\text{revenue}_m - \text{revenue}_{m-1}}{\text{revenue}_{m-1}}
$$

Both divide by something that can be zero. Returning `NaN` rather than infinity or zero keeps "undefined" separate from "no change", and downstream code can test for it.

### Ties need a rule

"The region with the highest revenue" is ambiguous when two regions tie. Sorting by revenue descending and then by region name makes the choice reproducible, which is what lets a test (or a reconciled report) give the same answer twice.

### Verifying a pipeline

A good habit: reconcile totals at each stage. Total revenue after the join should equal the sum over months; the number of orders should equal the rows that survived parsing and the join. When a number does not reconcile, the lost rows are in exactly one stage.

### How pandas actually implements this

Each step is vectorised: `to_datetime` parses in compiled code, `merge` is a hash join, `groupby` factorises keys into integer codes, `reindex` aligns by index (a sorted merge), and `shift` just offsets the underlying array by one position. Chaining them costs a few passes over the data, not a Python loop per row.

## Explanation

`monthly_report` parses `order_date` with `errors="coerce"` and drops the `NaT` rows, inner-joins the customers to get each order's region (unknown customers disappear), and derives the month start with `dt.to_period("M").dt.to_timestamp()`. It aggregates count and revenue per month, then `reindex`es onto a continuous month-start calendar so empty months appear, converting their missing count and revenue to `0`. The average divides by the count only where it is positive; the growth compares each month with `shift(1)` and is `NaN` where the previous revenue is not positive. For the top region it sums revenue per (month, region), orders by month, revenue descending and region ascending, and keeps the first row of each month.
