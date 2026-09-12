---
name: ensembles-adaboost
title: 'AdaBoost: reweighting misclassified samples each round'
tags: [classical-ml, ensembles, boosting]
difficulty: Intermediate
---

## Statement

Implement:

```python
def adaboost_train(input, labels, n_rounds, max_depth=1, seed=None) -> list[tuple[dict, float]]: ...
def adaboost_predict(ensemble, input) -> np.ndarray: ...
```

- `labels` are `{-1, +1}`-valued, AdaBoost's standard convention, not `{0, 1}`.
- Reuse `03-best-split-minimal-tree`'s `build_tree`/`predict_tree`, don't reimplement tree construction.
- `max_depth=1` by default, a shallow "decision stump," AdaBoost's classic weak learner.

## Theory

Gradient boosting (`03`/`04` in this track) corrects mistakes by fitting a new tree to the _residual_. AdaBoost, an earlier and differently-shaped boosting algorithm, corrects mistakes a different way: it doesn't change what the next learner predicts, it changes _which training samples the next learner is trained to care about_.

Every sample starts with equal weight, `1/n_samples`. Each round: train a weak learner (a shallow tree) on a resample of the data drawn according to the current weights, so heavily-weighted samples are more likely to appear. Measure that learner's _weighted_ error rate, then give it a vote strength `alpha`:

```text
alpha = 0.5 * log( (1 - weighted_error) / weighted_error )
```

A learner that does much better than chance (`weighted_error` near 0) gets a large positive `alpha`, a strong vote. A learner barely better than a coin flip (`weighted_error` near 0.5) gets `alpha` near 0, its vote barely counts at all.

Then, the actual "reweighting" the title names: every sample the current round got _wrong_ has its weight increased, every sample it got _right_ has its weight decreased, so the next round's resample is more likely to include exactly the samples this round struggled with.

```text
weight *= exp(-alpha * true_label * prediction)
```

When `true_label` and `prediction` agree (both `+1` or both `-1`, so their product is `+1`), the exponent is negative, weight shrinks. When they disagree (product is `-1`), the exponent is positive, weight grows. Weights are renormalized to sum to `1` after every round, so they always remain a valid distribution to resample from.

The final prediction is a weighted vote across every round's tree, `sign(sum(alpha_i * tree_i(x)))`, rounds with a stronger `alpha` (a more accurate weak learner) count for more.

## Explanation

`adaboost_train` resamples `input`/`labels` by `weights` (`rng.choice(..., p=weights)`), not uniformly, this is what makes the weak learner actually pay more attention to previously-hard samples, then `build_tree` on that resample the normal way. The weighted error is measured on the _full_ original data, `predictions != labels`, `weights[incorrect].sum()`, since the resample is just a training mechanism, evaluation needs to reflect every sample's true current importance.

`np.clip(weighted_error, 1e-10, 1 - 1e-10)` guards `alpha`'s formula against `log(0)` or a division by zero, an error rate of exactly `0` or `1` is a real edge case a small, discrete decision stump can hit.

`weights *= np.exp(-alpha * labels * predictions)` is the single line that does the reweighting, `labels * predictions` is `+1` when they agree and `-1` when they don't, exactly the mechanism Theory describes. Renormalizing (`weights / weights.sum()`) after every round keeps `weights` a valid probability distribution for the next round's resampling.

`adaboost_predict` accumulates `alpha * predict_tree(tree, input)` across every round (each individual prediction is `-1` or `+1`, scaled by that round's vote strength), then `np.sign(...)` collapses the weighted sum back down to a single `{-1, +1}` decision.
