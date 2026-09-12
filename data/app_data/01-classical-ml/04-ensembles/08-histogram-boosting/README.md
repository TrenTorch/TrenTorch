---
name: ensembles-histogram-boosting
title: 'Note: histogram-based boosting (LightGBM-style binning), why it is faster at scale'
tags: [classical-ml, ensembles, gradient-boosting, scalability]
difficulty: Beginner
---

## Statement

Implement:

```python
def build_histogram(values: np.ndarray, n_bins: int) -> np.ndarray:
    """n_bins + 1 evenly-spaced bin edges covering [values.min(), values.max()]."""

def find_best_split_histogram(input, labels, n_bins) -> tuple[int, float, float] | None:
    """Like find_best_split, using only n_bins-1 candidate thresholds per feature."""
```

- Reuse `02-information-gain`'s `information_gain`, the scoring itself doesn't change, only which thresholds get scored.

## Theory

`03-best-split-minimal-tree`'s `find_best_split` tries a candidate threshold between _every_ pair of consecutive unique values in a feature. That's exact, but its cost scales with how many distinct values the feature has, on a real column with a million distinct floating-point values, that's a million candidate thresholds to evaluate, for every feature, at every node, every round of boosting.

**Histogram-based** methods (LightGBM's core idea, though its full implementation adds more, like gradient-based one-side sampling and exclusive feature bundling) sidestep this by discretizing each feature into a small, fixed number of bins first, `n_bins` might be `255`, regardless of whether the feature actually has `50` or `50` million distinct values, then only ever considering the boundaries _between bins_ as candidate thresholds.

```text
exact search:      candidate thresholds = (number of distinct values) - 1
histogram search:   candidate thresholds = n_bins - 1, always, no matter the data
```

This trades a small amount of split precision (the best split might fall inside a bin rather than exactly at the best possible boundary) for a huge, _predictable_ speed advantage: the search cost per feature per node stops depending on dataset size at all. This is why gradient boosting libraries built for large datasets (LightGBM, and XGBoost's `hist` tree method) default to histogram-based splitting rather than the exact method `03-best-split-minimal-tree` implements, exact search is the more precise algorithm, histogram search is the one that actually finishes on a hundred-million-row dataset.

## Explanation

`build_histogram` is `np.linspace(values.min(), values.max(), n_bins + 1)`, `n_bins` intervals need `n_bins + 1` boundary points, exactly what `np.linspace`'s count argument means.

`find_best_split_histogram` mirrors `find_best_split`'s structure exactly, same feature loop, same `information_gain` scoring, same "track the best (feature, threshold, gain) seen" pattern, the only change is `candidate_thresholds = edges[1:-1]`, the interior bin edges only (the first and last edges are `values.min()`/`values.max()` themselves, using either as a threshold puts every sample on one side, not a real split). Regardless of how many rows `input` has or how many distinct values a feature contains, this inner loop always runs exactly `n_bins - 1` times per feature, this is the entire speed argument made concrete: candidate-threshold count is now a knob you set (`n_bins`), not a property of the data you're stuck with.
