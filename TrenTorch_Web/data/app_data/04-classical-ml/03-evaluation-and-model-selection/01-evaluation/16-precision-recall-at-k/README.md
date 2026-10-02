---
name: evaluation-precision-recall-at-k
title: Precision@k and Recall@k
tags: [classical-ml, evaluation, ranking]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Search and recommendation systems return a ranked list, and only the top few results are ever seen. Precision@k asks how much of the top k is relevant; Recall@k asks how much of everything relevant made it into the top k.

### From theory to code

Implement `precision_at_k(ranked, relevant, k)` and `recall_at_k(ranked, relevant, k)`.

### Constraints

- `ranked` is a list of item ids, best first; `relevant` is a collection of the truly relevant ids.
- `precision_at_k` divides by `k` even if `ranked` is shorter than `k`; return `0.0` when `k <= 0`.
- `recall_at_k` divides by the number of relevant items; return `0.0` when there are none, or when `k <= 0`.
- Both return Python floats.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Slice `ranked[:k]` and count how many of those ids are in the relevant set.

</details>

<details><summary>Hint 2</summary>

The two metrics share the hit count and differ only in the denominator.

</details>

## Theory

### The simple version

Precision@k punishes junk in the top k. Recall@k punishes relevant things missing from it. Making k larger tends to raise recall and lower precision.

### The formula

$$\text{Precision@}k = \frac{|\text{top-}k \cap \text{relevant}|}{k}, \qquad \text{Recall@}k = \frac{|\text{top-}k \cap \text{relevant}|}{|\text{relevant}|}$$

### How libraries implement this

Ranking libraries such as `torchmetrics` (`RetrievalPrecision`, `RetrievalRecall`) implement these per query and average across queries.

## Explanation

Converting `relevant` to a `set` makes membership checks constant-time. Dividing precision by `k` rather than by the list length is the standard definition: a short list is penalised for the slots it left empty.
