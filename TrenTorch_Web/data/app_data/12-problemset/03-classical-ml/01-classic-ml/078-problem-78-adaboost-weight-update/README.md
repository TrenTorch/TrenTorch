---
name: problem-78-adaboost-weight-update
title: 'AdaBoost Weight Update'
tags: [problemset, classical-ml-trees-ensembles, boosting]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'boosting'
hint: 'alpha = 0.5*ln((1-err)/err); w *= exp(-alpha*y*h); normalise'
tools: [NumPy]
---

## Statement

Perform the AdaBoost sample-weight update for one boosting round. Labels `y` and the weak learner's predictions `h` are in $\{-1,+1\}$, `weights` are the current sample weights and `error` is the weighted error of the learner. Increase the weight of misclassified samples, decrease the others, and renormalise.

Implement `solve(y, h, weights, error)`.

**Returns.** Return a new NumPy array of weights that sums to 1. The `weights` argument is not modified. The error is clamped below at $10^{-15}$ so a perfect learner does not divide by zero.

### Examples

**Example 1**

Input:

```python
solve([1, 1, -1, -1], [1, -1, -1, -1], [0.25, 0.25, 0.25, 0.25], 0.25)
```

Output:

```text
[0.166667, 0.5, 0.166667, 0.166667]
```

**Example 2**

Input:

```python
solve([1, -1], [1, -1], [0.5, 0.5], 0.5)
```

Output:

```text
[0.5, 0.5]
```

## Theory

### The simple version

AdaBoost trains weak learners one after another, each time focusing on the samples the previous ones got wrong. It does that by re-weighting: mistakes become heavier, correct samples lighter, so the next learner is forced to care about the hard cases.

### The formulas

$$\alpha=\tfrac12\ln\frac{1-\varepsilon}{\varepsilon},\qquad w_i\leftarrow\frac{w_i\,e^{-\alpha\,y_ih_i}}{\sum_j w_je^{-\alpha\,y_jh_j}}$$

## Explanation

When $y_ih_i=+1$ (correct) the factor $e^{-\alpha}$ shrinks the weight; when $-1$ (wrong) the factor $e^{\alpha}$ grows it. A learner no better than chance ($\varepsilon=0.5$) has $\alpha=0$, so the weights do not change, as the second example shows. In the first example the single misclassified sample ends up with weight $0.5$.
