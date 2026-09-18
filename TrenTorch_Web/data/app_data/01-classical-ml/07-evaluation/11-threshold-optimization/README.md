---
name: evaluation-threshold-optimization
title: 'Threshold optimization for imbalanced classification'
tags: [classical-ml, evaluation, imbalanced-data]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every classifier that outputs a probability or score, logistic regression's `sigmoid`, a tree's leaf fraction, needs a threshold to turn that score into an actual `0`/`1` decision: `predictions = scores >= threshold`. `0.5` is the default nearly every library reaches for, and it's a completely arbitrary choice, nothing in the model's math requires it.

`0.5` is a particularly bad default on imbalanced data. With, say, 5% positive examples, a model can predict "negative" for almost everything and still look fine at that threshold, because there simply aren't many positive examples for a wrong threshold to visibly hurt. But nothing says the threshold has to stay fixed: it's a hyperparameter exactly like `04-grid-search`'s `lr` or `depth`, and it can be swept and optimized the same way, against whatever metric actually matters for the problem, F1, balanced accuracy, or something task-specific, rather than left at a default nobody chose with this dataset in mind.

### From theory to code

Theory frames the threshold as a hyperparameter to sweep: try candidate thresholds, score the resulting predictions, keep the best. Implement `f1_metric(labels, predictions)`, a small wrapper reusing `02-classification-metrics`'s `precision_recall_f1`, and `optimize_threshold(labels, scores, metric_fn=f1_metric)`, which runs that sweep over the scores actually produced by the model.

### Constraints

- `f1_metric(labels, predictions) -> float`: reuse `02-classification-metrics`'s `precision_recall_f1`, return only the F1 value.
- `optimize_threshold(labels, scores, metric_fn=f1_metric) -> (best_threshold, best_score)`.
- Candidate thresholds are exactly the distinct values in `scores` (`np.unique(scores)`), not an arbitrary fixed grid like `0.0, 0.1, ..., 1.0`.
- `metric_fn(labels, predictions) -> float`: higher is always better.
- `predictions` passed to `metric_fn` come from `(scores >= threshold).astype(int)`.
- Return the threshold achieving the strictly highest `metric_fn` score, and that score itself.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

There's no reason to test a threshold value that isn't a score the model actually produced, any two thresholds between the same pair of adjacent distinct scores give identical predictions. `np.unique(scores)` already gives you every threshold worth trying.

</details>

<details>
<summary>Hint 2</summary>

This is the same "loop, evaluate, keep the best" shape as `04-grid-search`'s `grid_search`, just over a single continuous value instead of a grid: track a running best threshold and best score, updating only when a candidate beats the current best.

</details>

## Theory

### The simple version

Picture a smoke detector that beeps whenever it's more than 50% sure there's smoke. If real fires are rare, that sensitivity might let a genuine fire slip past without ever crossing 50%, an under-alarmed detector. Turning the sensitivity down (lowering the threshold) catches more real fires at the cost of more false alarms, and somewhere in that tradeoff is a setting that's actually best for the situation, not automatically 50%. Optimizing a classification threshold is the exact same dial, tuned against real data instead of guessed.

### The formula

```text
for threshold in unique(scores):
    predictions = (scores >= threshold)
    score = metric_fn(labels, predictions)
    keep threshold if score is the best seen so far
return best_threshold, best_score
```

`f1_metric` is a specific `metric_fn`:

```text
f1_metric(labels, predictions) = precision_recall_f1(labels, predictions)[2]
```

### How PyTorch actually implements this

PyTorch's classification metrics (`torchmetrics.F1Score`, `torchmetrics.PrecisionRecallCurve`) compute F1 or precision/recall at a threshold you supply, they don't search for the best one themselves; a threshold sweep like this is typically written by hand on top, iterating candidate thresholds and picking the one that maximizes whatever metric matters, exactly the loop `optimize_threshold` implements.

## Explanation

`f1_metric` in `solution.py` is a one-line wrapper: `_, _, f1 = precision_recall_f1(labels, predictions); return f1`, discarding precision and recall and keeping only the third returned value. It's the default `metric_fn` for `optimize_threshold` because F1 balances precision and recall in one number, rather than forcing the caller to pick just one to optimize.

`optimize_threshold` computes `thresholds = np.unique(scores)`, then initializes `best_threshold, best_score = float(thresholds[0]), float("-inf")` before looping over every candidate: `predictions = (scores >= threshold).astype(int)`, `score = metric_fn(labels, predictions)`, updating `best_threshold`/`best_score` only `if score > best_score`, a strict inequality, so ties keep the first (lowest) threshold encountered rather than the last. `tests.py`'s `test_optimize_threshold_picks_the_maximum_not_the_minimum` checks this loop tracks the best, not the worst, score seen, and `test_optimizing_the_threshold_improves_f1_on_imbalanced_data` verifies the concrete payoff Theory describes: on data built with only 5% positives, `optimize_threshold`'s chosen threshold beats the default `0.5`'s F1 score.
