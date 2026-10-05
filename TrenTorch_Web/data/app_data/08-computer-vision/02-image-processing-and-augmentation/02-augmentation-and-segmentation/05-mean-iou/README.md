---
name: vision-mean-iou
title: Confusion Matrix & Mean IoU
tags: [computer-vision, segmentation, metrics]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The standard score for semantic segmentation is **mean intersection over union**. For each class, take the pixels predicted as that class and the pixels that truly belong to it; IoU is the size of their overlap divided by the size of their union. Averaging over classes gives mIoU. Everything is read off a **confusion matrix** whose entry `C[i, j]` counts pixels with true class `i` predicted as class `j`: the diagonal holds correct pixels, a row sum is the true size of a class and a column sum is its predicted size. A class that never occurs and is never predicted has an undefined IoU (0/0) and is excluded from the mean.

### From theory to code

Implement `confusion_matrix` and `mean_iou`.

### Constraints

- `confusion_matrix(pred, target, n_classes)` takes integer arrays of equal shape with values in `0..n_classes-1` and returns an `(n_classes, n_classes)` integer matrix with `C[true, pred]` counts.
- `mean_iou(conf)` computes per-class `IoU_c = C[c, c] / (row_sum_c + col_sum_c - C[c, c])` and returns `(miou, ious)`, where classes with a zero denominator get `nan` in `ious` and are ignored by the mean (`np.nanmean`).

### Hints

<details>
<summary>Hint 1</summary>

A single `np.bincount(target * n + pred, minlength=n * n)` builds the matrix without a loop.

</details>

<details>
<summary>Hint 2</summary>

Check the denominator before dividing, so no divide-by-zero warning appears.

</details>

## Theory

### The simple version

For each category, how much of the territory you drew overlaps the true territory, relative to everything either of you claimed. Averaging over categories keeps a rare class as important as the sky.

### The formula

$$
\text{IoU}_c = \frac{C_{cc}}{\sum_j C_{cj} + \sum_i C_{ic} - C_{cc}} = \frac{TP}{TP + FP + FN}, \qquad
\text{mIoU} = \frac{1}{|\mathcal{C}'|}\sum_{c \in \mathcal{C}'}\text{IoU}_c
$$

### How this is done in practice

Cityscapes, ADE20K and Pascal VOC all report mIoU. Frameworks accumulate the confusion matrix over the whole validation set and compute IoU at the end; averaging per-image IoUs gives a different, less standard number.

## Explanation

The matrix is a bincount of a combined index. Per-class IoU then uses only row sums, column sums and the diagonal, which is why the confusion matrix is the single object a segmentation evaluator needs.
