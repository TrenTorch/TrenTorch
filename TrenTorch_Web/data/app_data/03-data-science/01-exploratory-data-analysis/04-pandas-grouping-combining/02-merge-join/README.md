---
name: data-science-pandas-merge-join
title: Merge & Join
tags: [data-science, pandas, merge, join]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Real data lives in several tables: customers in one, their orders in another, the products in a third. Combining them is what a `merge` (SQL's `JOIN`) does, and most of the ways it goes wrong are silent. Rows vanish because a key had no partner. Rows multiply because a key had _two_ partners. A "left" join keeps a customer who never ordered, but fills their order columns with `NaN`, and an `int` count turns into a `float`.

This question builds the four join questions an analyst is asked constantly: the orders with their customer, every customer with their order totals (including those with none), the customers who never ordered (an anti-join), and a merge that refuses to run if it would multiply rows by accident.

### From theory to code

Implement `orders_with_customers(customers, orders)`, `customer_totals(customers, orders)`, `customers_without_orders(customers, orders)` and `safe_merge(left, right, key)`. The signatures and docstrings are already in the editor.

### Constraints

- `customers` has columns `id` (unique), `name`, `city`. `orders` has `order_id` (unique), `customer_id`, `amount`. Keys are never missing. An order may refer to a customer that does not exist.
- `orders_with_customers(customers, orders)` is the **inner** join of the two tables on `orders.customer_id == customers.id`. It returns only the columns `order_id`, `customer_id`, `name`, `amount` (in that order), sorted by `order_id`, with a fresh `0..n-1` index.
- `customer_totals(customers, orders)` returns one row per customer with the columns `id`, `name`, `n_orders` (integer count of the customer's orders) and `total` (sum of their `amount`). A customer with no orders appears with `n_orders = 0` and `total = 0.0`. Sorted by `id`, fresh `0..n-1` index.
- `customers_without_orders(customers, orders)` returns the rows of `customers` (all of their columns, in their original order) whose `id` appears in no order, with a fresh `0..n-1` index.
- `safe_merge(left, right, key)` returns the **left** join of `left` with `right` on the column `key`, keeping `left`'s row order, with a fresh index. If `right` has the same `key` value more than once it must raise `ValueError` instead of multiplying rows.

### Hints

<details>
<summary>Hint 1</summary>

`merge(..., left_on=..., right_on=...)` joins on columns with different names. `how` chooses inner, left, right or outer.

</details>

<details>
<summary>Hint 2</summary>

Aggregate the orders per customer first, then left-join the totals onto the customers and fill the gaps for the customers with no orders.

</details>

<details>
<summary>Hint 3</summary>

`merge` has an `indicator` argument that records which side each row came from, and a `validate` argument that checks the relationship (such as `"m:1"`, many left rows to one right row).

</details>

## Theory

### The simple version

A guest list and a table of RSVPs. An **inner** join is "guests who replied". A **left** join is "every guest, with their reply if they sent one". An **anti-join** is "guests who did not reply". And if two replies came in under the same guest's name, the guest appears twice. That last one is the surprise worth remembering.

### Join types

| `how`   | Keeps           | Unmatched rows         |
| ------- | --------------- | ---------------------- |
| `inner` | keys in both    | dropped                |
| `left`  | every left row  | right columns `NaN`    |
| `right` | every right row | left columns `NaN`     |
| `outer` | every key       | the missing side `NaN` |

An **anti-join** (left rows with no partner) has no `how` of its own. Use a left join with `indicator=True` and keep the rows marked `left_only`, or test membership with `isin`.

### How many rows come out

If a key occurs $a$ times on the left and $b$ times on the right, the join produces $a \times b$ rows for that key. With unique keys on one side ($a$ or $b$ is 1) the row count never grows. With duplicates on both, it multiplies, and a "total revenue" quietly doubles. Declaring the expected relationship makes the merge check it: `validate="1:1"`, `"m:1"`, `"1:m"` raise `MergeError` (a `ValueError`) when it does not hold.

### Types change when rows go missing

A left join leaves `NaN` where there was no match, and `NaN` is a float, so an integer column such as `n_orders` becomes `float64`. Fill the gaps _and_ cast back (`fillna(0).astype(int)`) if the column should stay an integer.

### Aggregate before you join

To attach per-customer totals, summarise the orders to one row per customer first and join that. Joining first and aggregating afterwards works too, but it carries every order row through the join, which is more memory and easier to get wrong.

### How pandas actually implements this

`merge` factorises the join keys of both sides into shared integer codes, builds indexers for the left and right rows that match (a hash join), and uses them to _take_ rows from each table, concatenating the columns. The result of a `many-to-many` key is the cross product of the matching rows, which is why validating the relationship up front is cheap insurance.

## Explanation

`orders_with_customers` is an inner `merge` with `left_on="customer_id"`, `right_on="id"`, then selects the four columns, sorts by `order_id` and resets the index. `customer_totals` aggregates the orders to one row per customer, left-joins that onto the customers, fills the missing counts and totals with `0` and casts the count back to `int`. `customers_without_orders` keeps the customers whose `id` is not in the orders' `customer_id` column. `safe_merge` is a left `merge` with `validate="m:1"`, which raises when the right side has a duplicated key (a `MergeError`, a subclass of `ValueError`).
