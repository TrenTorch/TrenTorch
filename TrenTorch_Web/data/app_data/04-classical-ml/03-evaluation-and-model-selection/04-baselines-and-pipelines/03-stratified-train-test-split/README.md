---
name: evaluation-stratified-train-test-split
title: Stratified train-test split
tags: [classical-ml, evaluation, splitting]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Suppose 5 percent of your examples are positive. A random split can, by chance, put almost all of them in one side, and then your test set says little about how the model handles the rare class. A stratified split fixes the class proportions on both sides: each class is split separately, so the test set keeps the same mix as the full dataset.

Implement `stratified_train_test_split(y, test_fraction=0.25, seed=0)`, which returns `(train_indices, test_indices)` as sorted integer arrays. Each class is shuffled with a seeded generator and `round(test_fraction * class_count)` of its members go to the test set.

### Constraints

- Every index appears in exactly one of the two outputs.
- For each class, the number of test examples is `round(test_fraction * class_count)`.
- `test_fraction` must lie in `[0, 1]`, otherwise raise `ValueError`.
- The same `seed` gives the same split.
- Both outputs are sorted.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.flatnonzero(y == label)` gives the indices of one class. Shuffle those indices with `rng.shuffle`.

</details>

<details>
<summary>Hint 2</summary>

The first `n_test` shuffled indices go to test, and the rest go to train. Concatenate the pieces across classes and sort at the end.

</details>

## Theory

### The simple version

Split each class on its own, then combine. Both sides then carry the same class proportions as the whole dataset, so a rare class is never accidentally left out of the test set.

### The formula

For class $c$ with $n_c$ members, the number in the test set is

$$
n_{\text{test},c} = \operatorname{round}(f \cdot n_c)
$$

where $f$ is `test_fraction`. This keeps each class's share within one example of $f$ on the test side.

## Explanation

`stratified_train_test_split` validates the fraction, loops over the sorted unique labels, shuffles each class's indices with a generator seeded from `seed`, sends the first `round(f * n_c)` shuffled indices to test, and the rest to train. Sorting the concatenated outputs gives a stable, readable result.
