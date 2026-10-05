---
name: evaluation-majority-class-baseline
title: Majority-class baseline
tags: [classical-ml, evaluation, baselines]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Before trusting any classifier, you need to know what it has to beat. A model that reaches 92 percent accuracy sounds strong until you notice that 92 percent of the labels were the same class. The majority-class baseline predicts the most frequent training label for every example. Any real model should clear it.

Implement `majority_class_baseline(y_train, n_samples)`, which returns an array of length `n_samples` filled with the most frequent label in `y_train`.

### Constraints

- When two labels tie for most frequent, return the smaller label (the first in sorted order).
- `y_train` must not be empty: raise `ValueError`.
- The returned array has the same dtype as `y_train`.
- Do not modify `y_train`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.unique(y_train, return_counts=True)` gives sorted labels and their counts.

</details>

<details>
<summary>Hint 2</summary>

`np.argmax` returns the first index of the maximum, which is the smallest tied label after sorting.

</details>

## Theory

### The simple version

Always guess the crowd's favorite answer. It ignores every feature, so it is the cheapest possible classifier. Its accuracy equals the frequency of the majority class, which is the bar every model has to clear.

### The formula

$$
\hat{y} = \arg\max_c \; \lvert \{ i : y_i = c \} \rvert
$$

## Explanation

`majority_class_baseline` counts each label, picks the label with the largest count using `np.argmax` on the sorted labels, and repeats it `n_samples` times with the input dtype. Sorting before `argmax` is what makes ties resolve deterministically to the smaller label.
