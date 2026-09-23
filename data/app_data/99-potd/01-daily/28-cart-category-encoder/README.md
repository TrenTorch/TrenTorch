---
name: potd-cart-category-encoder
title: 'CART CATEGORY ENCODER'
tags: [classical-ml, data-processing]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Classic ML, Data Processing

---

### Story

Instacart's substitution-suggestion model needs the categorical product-department column encoded
before it can touch a single row of cart data. This is the same mechanic as the Airbnb amenity
question, different domain, because this exact operation shows up constantly across real pipelines.

---

### The Math

One-hot encode a categorical column into an `n x k` binary matrix, `k` the number of distinct
categories, columns alphabetical.

### Input Format

```
n
dept_1
...
dept_n
```

### Output Format

First line: distinct departments alphabetically. Next `n` lines: one-hot rows.

### Constraints

- `1 <= n <= 10^4`
- Time limit: 1.0 second.

---

### Example

**Input**

```
4
dairy
produce
dairy
bakery
```

**Output**

```
bakery dairy produce
0 1 0
0 0 1
0 1 0
1 0 0
```

## Theory

### The simple version

Same idea as the Airbnb amenity question: turn a category name into a column of its own, with a 1 marking which category each row belongs to.

### Same convention as the amenity encoder

This is the identical encoding rule (alphabetical column order, one-hot per row) applied to a
different column. Recognizing the shared mechanic and reusing the same approach, rather than
writing bespoke logic from scratch, is the point of this pairing.

### `k = n`, every row a distinct department

When every row is its own distinct department, `k = n`, and the encoder must not assume the number
of distinct categories is small relative to `n`.

### Shared prefixes are still distinct strings

`"dairy"` and `"dairy_alt"` share a prefix but are unrelated categories; they must sort and encode
as two entirely separate columns, not be merged by any kind of prefix matching.

## Explanation

`encode_departments` follows the same structure as the amenity one-hot encoder: sort the distinct
department strings with `sorted(set(depts))` for the alphabetical column order, build a
`department -> column index` dictionary from that sorted list, then set one `1` per row at the
matching column. String comparison in Python is exact and prefix-agnostic, so `"dairy"` and
`"dairy_alt"` never collide regardless of how many characters they share.
