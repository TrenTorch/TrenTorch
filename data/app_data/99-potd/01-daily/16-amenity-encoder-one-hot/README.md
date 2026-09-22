---
name: potd-amenity-encoder-one-hot
title: 'AMENITY ENCODER'
tags: [data-processing, classical-ml]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Data Processing, Classic ML

---

### Story

Every Airbnb listing carries a categorical amenities tag, and the pricing model cannot consume raw
strings. This is the encoding step that runs before every single downstream feature touches the
model.

---

### The Math

One-hot encode a categorical column of `n` values into an `n x k` binary matrix, where `k` is the
number of **distinct** categories present, columns ordered alphabetically.

### Input Format

```
n
cat_1
cat_2
...
cat_n
```

### Output Format

First line: the `k` distinct categories, alphabetically, space-separated. Next `n` lines: the
one-hot row for each input, space-separated `0`/`1`.

### Constraints

- `1 <= n <= 10^4`, category strings up to 20 characters
- Time limit: 1.0 second.

---

### Example

**Input**

```
5
wifi
parking
wifi
pool
parking
```

**Output**

```
parking pool wifi
0 0 1
1 0 0
0 0 1
0 1 0
1 0 0
```

## Theory

### The simple version

A model cannot do arithmetic on the word "wifi." One-hot encoding turns each category into its own on/off column, so "wifi" becomes a 1 in the wifi column and 0 everywhere else.

### Column order is alphabetical, not first-appearance

Sorting the distinct categories alphabetically before assigning them columns is the detail most
naive solutions get wrong: building columns in the order categories first appear produces a
different, equally "plausible"-looking layout that does not match this problem's convention.

### Case sensitivity

`"Wifi"` and `"wifi"` are distinct categories here, no normalization. Silently lowercasing the input
would merge categories the problem intends to keep separate.

### High cardinality

With up to `n` distinct categories, a lookup from category string to column index needs to be a
dictionary, not a linear scan through the list of known categories for every row; the latter
degrades to roughly `O(n * k)` at high cardinality.

## Explanation

`one_hot_encode` first collects the distinct categories with `sorted(set(categories))`, giving the
alphabetical column order directly. It builds a `category -> column index` dictionary from that
sorted list, then for each input row sets a `1` at that category's column and `0` elsewhere. Because
Python strings compare case-sensitively and the dictionary is keyed on the raw strings, `"Wifi"` and
`"wifi"` land in different columns without any special handling.
