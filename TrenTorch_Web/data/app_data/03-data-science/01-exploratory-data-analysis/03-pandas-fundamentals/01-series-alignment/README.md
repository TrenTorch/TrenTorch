---
name: data-science-pandas-series-alignment
title: Series, Index Alignment & Arithmetic
tags: [data-science, pandas, series]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A NumPy array knows its values and nothing else. A pandas `Series` carries a second thing with it, an **index** of labels, and that changes what arithmetic means. Add two arrays and the element at position 0 meets the element at position 0. Add two Series and the element labelled `"mon"` meets the element labelled `"mon"`, wherever each one happens to sit. This is called _index alignment_, and it is the reason a pandas calculation can silently give a different answer than the same numbers in an array: if a label appears on only one side, there is nothing to pair it with.

This question builds the four small operations that make alignment concrete: creating a labelled Series, adding two Series by label (with and without a fill value), turning values into shares of a total, and looking labels up without crashing on one that is not there.

### From theory to code

Implement `make_series(values, labels, name)`, `aligned_sum(a, b, fill_value=None)`, `share_of_total(s)` and `lookup(s, labels)`. The signatures and docstrings are already in the editor.

### Constraints

- `labels` are unique. `values` and `labels` have the same length.
- `make_series` returns a `pd.Series` with those values, that index (in the given order) and that name.
- `aligned_sum(a, b)` adds `a` and `b` by label. The result's index holds every label that appears in `a` or in `b`, sorted ascending. A label missing from one side gives `NaN`.
- `aligned_sum(a, b, fill_value=v)` treats a missing label **or** a `NaN` value on either side as `v` before adding. If both sides are missing or `NaN` for a label, the result for that label stays `NaN`.
- `aligned_sum` never changes `a` or `b`.
- `share_of_total(s)` returns a float Series with the same index and name as `s`, where each value is divided by the sum of the non-missing values. Missing values stay missing. The non-missing values do not sum to zero.
- `lookup(s, labels)` returns a Series indexed by `labels`, in that order, holding `s`'s value for each label and `NaN` for a label `s` does not have.

### Hints

<details>
<summary>Hint 1</summary>

Adding two Series with `+` already aligns on the index. What does it do to the order of the labels, and to a label present on one side only?

</details>

<details>
<summary>Hint 2</summary>

`Series.add` takes a `fill_value` argument that does the 'missing counts as v' step for you.

</details>

<details>
<summary>Hint 3</summary>

Selecting with `s[labels]` raises `KeyError` for an unknown label. A method that _conforms_ a Series to a new list of labels returns `NaN` instead.

</details>

## Theory

### The simple version

Picture two shopping receipts, each listing items and prices. To add them up item by item you match by **item name**, not by line number: the milk on receipt one goes with the milk on receipt two even if it is printed on line 1 and line 5. An item on only one receipt has no partner. A pandas Series is a receipt: values with names, and arithmetic always matches by name first.

### The data structure

A Series is two arrays held together:

$$
s = (	ext{values}[0..n-1],\ 	ext{index}[0..n-1])
$$

The index maps each label to a position. `s.loc["mon"]` finds the label's position and returns the value there. The index is itself an object with a type (strings, integers, timestamps), and it is what every later pandas operation (`join`, `groupby`, `resample`) uses to line rows up.

### Alignment

For a binary operation $a \mathbin{\square} b$ pandas first builds the union of the two indexes and **reindexes both** Series to it, then applies the operation position by position:

$$
(a + b)[\ell] = \begin{cases} a[\ell] + b[\ell] & \ell \in a,\ \ell \in b \\ \text{NaN} & \text{otherwise} \end{cases}
$$

This is why the result of `a + b` can have more entries than either input, and why a single misspelled label turns a sum into `NaN` instead of raising an error.

### Missing values

`NaN` (not a number) is how pandas marks "no value". It propagates: any arithmetic with `NaN` gives `NaN`. `fill_value` changes that on purpose, for one operation only, by substituting a number _before_ the operation. Aggregations such as `sum()` skip `NaN` by default, which is why a share computed as `s / s.sum()` leaves the missing entries missing and divides by the total of the known ones.

### Conforming to a list of labels

`reindex(labels)` returns a new Series whose index is exactly `labels`: labels already present keep their values, new ones become `NaN`, and labels not requested are dropped. It is how code lines data up with a fixed set of categories (every weekday, every product) even when some had no rows.

### How pandas actually implements this

`Series.__add__` calls `Series._align_for_op`, which uses `Index.union` (a sorted merge for sortable labels) and `Series.reindex` on both sides, then hands the two aligned arrays to NumPy. `Series.add(other, fill_value=...)` fills the _missing_ positions of each side before the NumPy call. The index lookup itself is a hash table (`Index.get_loc`), so finding a label is $O(1)$ on average rather than a scan.

## Explanation

`make_series` builds the Series from the lists, passing the labels as `index` and the `name`. `aligned_sum` is `a + b` when there is no fill value, since `+` aligns on the union of labels and gives `NaN` where a side is missing; with a fill value it calls `a.add(b, fill_value=...)`, which substitutes the fill for a missing label or a `NaN` value on either side and leaves `NaN` only when both are missing. Either result is sorted by label so the output order does not depend on the inputs' order. `share_of_total` converts to float and divides by the sum, which skips `NaN`, so missing entries stay missing. `lookup` is `s.reindex(labels)`, which returns `NaN` for a label the Series does not have where `s[labels]` would raise.
