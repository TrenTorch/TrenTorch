---
name: data-science-class-imbalance
title: Class Imbalance
tags: [data-science, classification]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-stratified-sampling` keeps the class mix when sampling an imbalanced dataset. Keeping the mix does not make the imbalance go away, and the imbalance is the problem. In fraud detection or disease screening, 99% of rows are one class, so a model that always predicts the majority class scores 99% accuracy and finds nothing. The standard remedies change what the model sees: weight the rare class more heavily in the loss, copy rare rows until the classes balance, throw away common rows, or invent new rare rows that lie between existing ones. This question builds all four.

### From theory to code

Implement `class_weights(y)`, which gives each class a loss weight inversely proportional to its frequency, then `random_oversample(X, y, rng)`, which duplicates minority rows, then `random_undersample(X, y, rng)`, which drops majority rows, then `interpolate_minority(minority, n_new, rng)`, which creates synthetic minority points between real ones. The signatures and docstrings are already in the editor.

### Constraints

- `X` is a 2D float array `(rows, features)` and `y` is a 1D array of class labels with one entry per row. `rng` is a `numpy.random.Generator`.
- `class_weights` returns a dict mapping each label to `n_samples / (n_classes * count_of_that_class)`. The weights of the classes, multiplied by their counts, all sum to the same total, so every class carries equal total weight.
- `random_oversample` returns new `(X_resampled, y_resampled)` arrays that keep every original row first, in order, then append extra rows for each class below the largest class count. For each such class in sorted label order, draw `needed = max_count - count` row indices with `rng.choice(rows_of_that_class, size=needed, replace=True)` and append those rows. Every class ends with `max_count` rows.
- `random_undersample` returns new `(X_resampled, y_resampled)` where every class is cut to the smallest class count. For each class in sorted label order, keep `rng.choice(rows_of_that_class, size=min_count, replace=False)` indices. The result lists the kept rows class by class in sorted label order, each class's rows sorted by original index.
- `interpolate_minority` takes a 2D array of minority-class points and returns an array of shape `(n_new, features)`. For each new point, in order, draw two distinct points `a` and `b` with `rng.choice(len(minority), size=2, replace=False)` and a weight `u = rng.random()` and return `a + u * (b - a)`. It needs at least 2 minority points.
- Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

Balanced weights make a class's weight times its count the same for every class, which is what "each class matters equally" means for a weighted loss.

</details>

<details>
<summary>Hint 2</summary>

Oversampling creates rows that are exact copies, so evaluating on a split made after oversampling would score the model on rows it already saw. Resample the training set only, after splitting.

</details>

<details>
<summary>Hint 3</summary>

A point on the line segment between two real minority points is a convex combination, so it always lies inside the region the minority class already occupies.

</details>

## Theory

### The simple version

A teacher grading a class where 99 of 100 students passed can mark everyone "pass" and be right 99% of the time without ever looking at an answer. To learn anything about the student who fails, the failing paper has to count for more: either by giving it a bigger weight, by photocopying it so it appears as often as the others, by setting aside most of the passing papers, or by writing a few more plausible failing papers in the same style. Those are the four moves here.

### The formula

**Balanced class weights.** For $n$ samples, $K$ classes and class $k$ with $n_k$ rows,

$$
w_k = \frac{n}{K\,n_k}
$$

so a class that makes up a small share gets a large weight, and $w_k\,n_k = n/K$ for every class. A weighted loss multiplies each row's loss by its class weight.

**Random oversampling** repeats minority rows (sampled with replacement) until every class has the majority count. **Random undersampling** keeps only as many rows of each class as the smallest class has.

**Interpolation (the idea behind SMOTE).** A synthetic point between two minority points $a$ and $b$ is

$$
x_{\text{new}} = a + u\,(b - a), \qquad u \sim \text{Uniform}(0, 1)
$$

which lies on the segment joining them.

### Trade-offs

Class weights change the loss and leave the data alone, so they are the cheapest and often the best first move. Undersampling discards real information. Oversampling by copying risks overfitting to repeated rows. Interpolation adds variety but can invent points that are not realistic when the minority class forms several separate clusters.

### Resample only the training set

Resampling must happen after the train/test split and touch only the training rows. Oversampling before the split puts copies of the same row on both sides, which is a leak that makes the test score look far better than it is. The test set should keep the real, imbalanced class mix, because that is the mix the model will meet in use.

### Accuracy is the wrong yardstick

On imbalanced data, report precision, recall, the area under the precision-recall curve or a cost-weighted measure. Always predicting the majority class scores high accuracy and zero recall.

### How NumPy/PyTorch actually implements this

`sklearn.utils.class_weight.compute_class_weight('balanced', ...)` computes exactly the weights above, and most estimators accept `class_weight='balanced'`. In PyTorch, `torch.nn.CrossEntropyLoss(weight=...)` and `torch.utils.data.WeightedRandomSampler` apply per-class weights to the loss and to the batches. The `imbalanced-learn` package provides `RandomOverSampler`, `RandomUnderSampler` and `SMOTE`.

## Explanation

`class_weights` counts each label with `np.unique(..., return_counts=True)` and applies `n / (K * count)`. `random_oversample` finds the largest class count and, for every smaller class in sorted label order, draws the missing number of row indices with replacement from that class, then appends the corresponding rows after all the original rows. `random_undersample` finds the smallest class count and, for every class in sorted label order, draws that many row indices without replacement, sorts them and concatenates the class blocks. `interpolate_minority` draws two distinct points and a uniform weight for each new point in turn and returns `a + u * (b - a)`, a point on the segment between them, with the draw order fixed so a seeded generator gives a reproducible result.
