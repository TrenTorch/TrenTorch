---
name: evaluation-classification-average-precision
title: 'Average precision'
tags: [classical-ml, evaluation, classification, ranking]
difficulty: Advanced
---

## Statement

### The problem, from first principles

A precision-recall curve needs a summary number for comparing models. Average precision (AP) is the area under that curve, computed as a step function: each time recall increases, add the precision at that point, weighted by how much recall increased. It rewards putting positives near the top of the ranking, and it is far more informative than ROC AUC when positives are rare.

Implement `average_precision(y_true, scores)` for binary labels, where higher score means more likely positive (label 1).

1. Sort rows by score, descending. Tied scores form one threshold: evaluate only after the last row of each tie group.
2. At each threshold, compute precision = TP / (TP + FP) and recall = TP / total positives.
3. AP = Σ (recall_k − recall_{k−1}) · precision_k, with recall_0 = 0.

### Constraints

- Inputs must have the same length, otherwise raise `ValueError`.
- If there are no positive labels, raise `ValueError`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.argsort(-scores, kind="stable")` orders the rows, and `np.cumsum` over the sorted labels gives TP at every row.

</details>

<details>
<summary>Hint 2</summary>

Keep only the positions where the sorted score changes, plus the last position. `np.diff(sorted_scores) != 0` finds the changes.

</details>

## Theory

### The simple version

Walk down the ranking. Every time you hit a positive, recall jumps up, and the precision you have at that moment counts toward the score in proportion to the jump. A perfect ranking puts every positive before every negative and scores 1.

### The formula

$$
\text{AP} = \sum_k (R_k - R_{k-1})\, P_k
$$

## Explanation

`average_precision` sorts the scores, takes cumulative true and false positive counts, and keeps only the cut points where the score changes so tied rows are judged together. It then sums recall gains weighted by precision at each cut point.
