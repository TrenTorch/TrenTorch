---
name: semi-supervised-co-training-selection
title: 'Choosing pseudo-labels in co-training'
tags: [classical-ml, semi-supervised, co-training, pseudo-labels, self-training]
difficulty: Intermediate
---

## Statement

### Pick confident pseudo-labels from two views

Co-training (Blum and Mitchell, 1998) trains two classifiers on two feature views of the same examples. Each classifier labels the unlabeled points it is confident about, and those labels become training data for the other. This question covers only the selection step.

Implement `pick_pseudo_labels(conf_a, pred_a, conf_b, pred_b, threshold)`.

- The four inputs are 1-D arrays of equal length `N`. `conf_*` holds each view's confidence in `[0, 1]`, and `pred_*` holds its predicted class.
- A point is selected when at least one view has confidence at least `threshold`.
- If only one view is confident, use its prediction.
- If both views are confident and agree, use that label.
- If both views are confident and disagree, skip the point.
- Return `(indices, labels)`: the selected indices in increasing order, and their labels.

### Constraints

- All four arrays have the same length. Otherwise raise `ValueError`.
- `threshold` must be in `(0, 1]`. Otherwise raise `ValueError`.
- Confidences must lie in `[0, 1]`. Otherwise raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Build two boolean masks, one per view, then combine them with `np.where` or explicit conditions. Skipping conflicts is a deliberate choice.

</details>

## Theory

Co-training works only when the two views are conditionally independent given the class and each view is good enough on its own. Selection is where errors enter, because a wrong pseudo-label is treated as ground truth in the next round. Requiring agreement when both views are confident is a conservative rule: it discards exactly the cases where one view is probably wrong, at the cost of fewer labels per round.

### Where this shows up in production

Co-training-style pipelines appear in systems that naturally have two views, such as an image classifier and an OCR text model on the same document, or a web-page text model and a URL model on the same link. A labeling team sets the threshold by reviewing a sample of accepted pseudo-labels, and the team monitors the rate of conflicts because a rising conflict rate often means a view has drifted.

### Using it to make decisions

Use co-training only if you can defend the two-view assumption on your data. Measure the accuracy of accepted pseudo-labels on a held-out labeled sample, not on training data. Start with a high threshold, since few confident errors are worth more than many noisy labels. Lower it only when the acceptance rate is too small to learn from, and stop when accepted-label accuracy falls.

### Pros and cons

**Pros:** cheap extra labels, a simple and auditable selection rule, and conflicts give an early warning of model disagreement.

**Cons:** if the views are correlated, the method reinforces shared mistakes, thresholds need calibrated confidences, and errors compound across rounds.

## Explanation

The solution computes two confidence masks and keeps only the points where at least one is set. Where both are set, it compares predictions and drops the disagreements, so a conflict never becomes training data.
