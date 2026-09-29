---
name: python-dicts-assemble-summarize-orders
title: 'Assemble: Summarize Customer Orders'
tags: [python-dicts, aggregation]
difficulty: Advanced
---

## Statement

Implement a single function that summarizes a list of nested order records into several dictionaries, combining counting, grouping, merging, nested access, comprehensions, and safe iteration.

## Theory

This problem introduces no new concepts. It combines this module's topics in one realistic data-processing task:

- Read nested dictionaries with `get` and iterate them with `items()`.
- Accumulate totals with `get(key, 0) + n` or `setdefault`.
- Group values by key into lists without sharing a list between keys.
- Pick a winner from a dictionary with a deterministic tie-break.
- Build derived dictionaries with comprehensions and leave the input untouched.

No new theory is required beyond re-reading those topics.

## Explanation

`summarize_orders` groups into `set`s while scanning orders (cheap membership checks, no manual "already in this list?" scan per item) and only converts each group to a `sorted` list once, at the very end, via a dictionary comprehension — this is also what guarantees no two keys share a list object, since `sorted()` always returns a brand-new list. `units_by_customer` gets a `setdefault(customer, 0)` entry unconditionally for every order, before looking at that order's items at all, so a customer whose every order is empty still ends up present with `0` rather than being silently absent. `top_sku` picks `min(...)` over the skus tied for the maximum quantity, which is exactly "alphabetically first among ties" without a separate sort-and-take-first step.
