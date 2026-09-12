---
name: evaluation-model-selection-class-imbalance
title: 'Model selection under class imbalance'
tags: [classical-ml, evaluation, imbalanced-data]
difficulty: Intermediate
---

## Statement

Implement:

```python
def balanced_accuracy(labels, predictions) -> float: ...
def stratified_k_fold_split(labels, k, seed=None) -> list[tuple[np.ndarray, np.ndarray]]: ...
```

## Theory

This track has already named two separate ways class imbalance breaks the _default_ tools: `02-classification-metrics`'s Theory notes plain accuracy hides a 95%-negative dataset's failure to catch positives at all, and `11-threshold-optimization` showed the default `0.5` threshold is rarely right for imbalanced data. Model _selection_ (choosing between models, or choosing hyperparameters via `04-grid-search`/`12-nested-cross-validation`) has two more of its own defaults that quietly break the same way:

**The scoring metric.** If `04-grid-search`'s `fit_and_score_fn` scores candidates by plain accuracy, it will happily select a hyperparameter setting that predicts the majority class almost always, that setting looks great by accuracy and is useless in practice. `balanced_accuracy`, the _average of each class's own recall_, doesn't have this blind spot: a model that ignores the minority class entirely gets `0%` recall on it, pulling the average down hard, regardless of how many majority-class samples it happens to get right.

**The cross-validation split itself.** `01-splitting-and-resampling`'s `k_fold_split` shuffles all samples together and slices, which is fine when classes are roughly balanced, but with a rare minority class, plain random folds can by bad luck put very few, or even zero, minority examples in some fold, making that fold's score meaningless (or undefined) purely by chance. `stratified_k_fold_split` fixes this by splitting _within_ each class separately first, then combining, guaranteeing every fold keeps close to the same class proportions as the whole dataset.

```text
plain k-fold:        shuffle everyone together, slice -- fold class ratios can vary by luck
stratified k-fold:    shuffle WITHIN each class, slice, then recombine -- every fold matches the overall ratio
```

Neither fix changes the model being trained at all, they change what "good" means when comparing candidates (`balanced_accuracy`) and how "different subsets of the same data" get constructed (`stratified_k_fold_split`), the same two places `04-grid-search`/`12-nested-cross-validation` already plug in a `score_fn` and a fold-splitting function.

## Explanation

`balanced_accuracy` computes, for each distinct class `c`, `recall_c = mean(predictions[labels == c] == c)`, the fraction of that class's own samples correctly identified, then averages those per-class recalls with `np.mean`, one vote per class regardless of class size, this is exactly what makes it insensitive to a majority class dominating a plain per-sample average.

`stratified_k_fold_split` builds `per_class_folds`, a dict keyed by class, where `per_class_folds[c]` is class `c`'s own shuffled indices split into `k` pieces (`np.array_split`, the same tool `01-splitting-and-resampling`'s `k_fold_split` uses, applied separately per class instead of once over everyone). For fold `i`, `val_idx` concatenates fold `i` from _every_ class, and `train_idx` concatenates every _other_ fold from every class, the same "one fold held out, the rest combined" shape `k_fold_split` uses, just assembled from per-class pieces so every fold's class mixture matches the whole dataset's.
