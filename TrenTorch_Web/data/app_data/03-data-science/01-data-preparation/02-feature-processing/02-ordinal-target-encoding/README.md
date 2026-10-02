---
name: data-science-ordinal-target-encoding
title: 'Ordinal & Target Encoding'
tags: [data-science, encoding]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-one-hot-encoding` turns a category into one column per value, which works until a column has thousands of values (a zip code, a product ID) and the table explodes. Two other encodings keep a single column. **Ordinal encoding** replaces each category by its rank when the categories have a natural order (small, medium, large). **Target encoding** replaces each category by the average of the label over the rows that have it, which packs the category's predictive signal into one number. Target encoding is also one of the easiest ways to leak the label into a feature by accident, so this question builds the safe versions.

### From theory to code

Implement `ordinal_encode(values, order)` for ordered categories, then `target_encode(categories, y, smoothing)`, which learns a smoothed mean per category, then `apply_target_encoding(categories, mapping, default)`, which uses a learned mapping, then `out_of_fold_target_encode(categories, y, n_folds, smoothing)`, which encodes every row using only rows from other folds. The signatures and docstrings are already in the editor.

### Constraints

- `values` and `categories` are 1D arrays of hashable labels. `y` is a 1D float array of the same length. `order` is a list of labels from lowest to highest.
- `ordinal_encode` returns an integer array where each value is the position of its label in `order`. A label that is not in `order` becomes `-1`.
- `target_encode` returns a dict mapping each category to `(n * category_mean + smoothing * global_mean) / (n + smoothing)`, where `n` is how many rows have that category and `global_mean` is the mean of all of `y`. With `smoothing = 0` this is the plain category mean.
- `apply_target_encoding` returns a float array with one value per entry of `categories`. A category missing from `mapping` gets `default`.
- `out_of_fold_target_encode` splits the row indices `0 .. n-1` into `n_folds` contiguous, nearly equal blocks with `np.array_split`, in order, with no shuffling. For each block it learns the mapping from all other rows with `target_encode` and applies it to the block, using the global mean of the other rows as `default`. It returns a float array of length `n`.

### Hints

<details>
<summary>Hint 1</summary>

The smoothing formula is a weighted average of two numbers: what this category's own rows say, and what the whole dataset says. A rare category has small `n`, so the global mean dominates, which stops one lucky row from setting a category's value.

</details>

<details>
<summary>Hint 2</summary>

A target encoding computed on all the rows includes each row's own label in the number that is then fed back as its feature. Computing it only from other folds removes that.

</details>

<details>
<summary>Hint 3</summary>

For the fold loop, build a boolean mask for the held-out block and call `target_encode` on the complement.

</details>

## Theory

### The simple version

A sizing chart has an order (S < M < L < XL), and ranking the sizes 0, 1, 2, 3 keeps that order in one column. A column of city names has no order, but each city has a track record: the share of its customers who bought. Replacing each city by its track record gives a model that signal directly. The danger is that a city seen only once has a track record of exactly 0 or 1, based on a single customer, and that a row's own outcome is part of its city's record.

### The formula

**Ordinal encoding** maps a label to its rank in a supplied order:

$$
\text{encode}(v) = \text{index of } v \text{ in the order}
$$

**Smoothed target encoding** maps a category $c$ with $n_c$ rows to

$$
\text{enc}(c) = \frac{n_c\,\bar{y}_c + m\,\bar{y}}{n_c + m}
$$

where $\bar{y}_c$ is the label mean within the category, $\bar{y}$ is the overall label mean and $m$ is the smoothing strength.

- With $m = 0$ this is the raw category mean. As $n_c$ grows the category's own mean takes over, and as $n_c$ shrinks the encoding falls back to the overall mean.
- It is a shrinkage estimate: the same idea as a prior pulling a noisy small-sample estimate toward a safe default.

### Why naive target encoding leaks

If the mapping is learned from every row and then applied to the same rows, each row's label contributes to its own feature value. For a category with few rows the feature nearly equals the label, so a model trained on it looks excellent in training and fails on new data. This is the same failure as `04-data-leakage`, arriving through a feature that was built from the target.

### Out-of-fold encoding

Split the rows into folds. Encode each fold using a mapping learned only from the other folds, so no row's label ever helps encode that row. The training feature is then built under the same conditions as the feature a new row will get at prediction time, when its own label is unknown. For the final model, the mapping learned from all training rows is applied to test data.

### How NumPy/PyTorch actually implements this

`sklearn.preprocessing.OrdinalEncoder(categories=[order])` is the ordinal encoder, with `handle_unknown='use_encoded_value', unknown_value=-1` for unseen labels. `sklearn.preprocessing.TargetEncoder` (scikit-learn 1.3 and later) is the smoothed target encoder and uses internal cross-fitting for exactly the leakage reason above. The `category_encoders` package offers the same families. `pandas.Categorical(values, categories=order, ordered=True).codes` is a one-line ordinal encoding.

## Explanation

`ordinal_encode` builds a dict from each label to its index in `order` and looks every value up with a default of `-1`, so unseen labels are flagged rather than raising. `target_encode` takes the global mean once, then for each unique category averages `y` over its rows and blends the two with the smoothing formula, using the row count as the weight on the category's own mean. `apply_target_encoding` is a dict lookup with a `default` for unseen categories. `out_of_fold_target_encode` splits `np.arange(n)` into contiguous blocks, and for each block builds the complement mask, learns a mapping from the complement only, and encodes the block with the complement's global mean as the fallback, so a row's label can never influence its own encoding.
