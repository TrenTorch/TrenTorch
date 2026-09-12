---
name: evaluation-model-selection-class-imbalance
title: 'Model selection under class imbalance'
tags: [classical-ml, evaluation, imbalanced-data]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

This track has already named two separate ways class imbalance breaks the *default* tools: `02-classification-metrics`'s Theory notes plain accuracy hides a 95%-negative dataset's failure to catch positives at all, and `11-threshold-optimization` showed the default `0.5` threshold is rarely right for imbalanced data. Model *selection* (choosing between models, or choosing hyperparameters via `04-grid-search`/`12-nested-cross-validation`) has two more of its own defaults that quietly break the same way.

### From theory to code

Implement `balanced_accuracy(labels, predictions)` and `stratified_k_fold_split(labels, k, seed=None)`. Neither changes the model being trained at all — they change what "good" means when comparing candidates, and how "different subsets of the same data" get constructed, the same two places `04-grid-search`/`12-nested-cross-validation` already plug in a `score_fn` and a fold-splitting function.

### Constraints

- `balanced_accuracy` returns the mean of each distinct class's own recall — one vote per class, regardless of class size.
- `stratified_k_fold_split` returns `k` `(train_idx, val_idx)` pairs, where every fold's class proportions match the overall dataset's proportions.
- Every sample appears in exactly one validation fold; train and validation indices never overlap within a split.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`balanced_accuracy` computes one recall value per class (`mean(predictions[labels == c] == c)`), then averages those — never a single pooled accuracy over all samples at once.

</details>

<details>
<summary>Hint 2</summary>

`stratified_k_fold_split` runs `01-splitting-and-resampling`'s own splitting idea *separately per class* first (shuffle each class's own indices, split into `k` pieces with `np.array_split`), then combines fold `i` across every class to build that fold's validation set.

</details>

## Theory

### The simple version

**The scoring metric.** If `04-grid-search`'s `fit_and_score_fn` scores candidates by plain accuracy, it will happily select a hyperparameter setting that predicts the majority class almost always — that setting looks great by accuracy and is useless in practice. `balanced_accuracy`, the *average of each class's own recall*, doesn't have this blind spot: a model that ignores the minority class entirely gets `0%` recall on it, pulling the average down hard, regardless of how many majority-class samples it happens to get right.

**The cross-validation split itself.** `01-splitting-and-resampling`'s `k_fold_split` shuffles all samples together and slices, which is fine when classes are roughly balanced, but with a rare minority class, plain random folds can by bad luck put very few, or even zero, minority examples in some fold, making that fold's score meaningless (or undefined) purely by chance. `stratified_k_fold_split` fixes this by splitting *within* each class separately first, then combining, guaranteeing every fold keeps close to the same class proportions as the whole dataset.

### The formula

```text
plain k-fold:        shuffle everyone together, slice -- fold class ratios can vary by luck
stratified k-fold:    shuffle WITHIN each class, slice, then recombine -- every fold matches the overall ratio
```

Neither fix changes the model being trained at all — they change what "good" means when comparing candidates (`balanced_accuracy`) and how "different subsets of the same data" get constructed (`stratified_k_fold_split`), the same two places `04-grid-search`/`12-nested-cross-validation` already plug in a `score_fn` and a fold-splitting function.

### How PyTorch actually implements this

Context only, untested by your submission: this is a general evaluation methodology, not a PyTorch operation — scikit-learn's `balanced_accuracy_score` and `StratifiedKFold` implement exactly these two fixes, and both apply identically when the model being scored is a PyTorch network rather than a classical one.

## Explanation

`balanced_accuracy` computes, for each distinct class `c`, `recall_c = mean(predictions[labels == c] == c)`, the fraction of that class's own samples correctly identified, then averages those per-class recalls with `np.mean` — one vote per class regardless of class size, this is exactly what makes it insensitive to a majority class dominating a plain per-sample average.

`stratified_k_fold_split` builds `per_class_folds`, a dict keyed by class, where `per_class_folds[c]` is class `c`'s own shuffled indices split into `k` pieces (`np.array_split`, the same tool `01-splitting-and-resampling`'s `k_fold_split` uses, applied separately per class instead of once over everyone). For fold `i`, `val_idx` concatenates fold `i` from *every* class, and `train_idx` concatenates every *other* fold from every class — the same "one fold held out, the rest combined" shape `k_fold_split` uses, just assembled from per-class pieces so every fold's class mixture matches the whole dataset's.
