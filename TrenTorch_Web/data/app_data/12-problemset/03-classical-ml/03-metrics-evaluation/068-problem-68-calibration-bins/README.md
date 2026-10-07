---
name: problem-68-calibration-bins
title: 'Calibration Bins'
tags: [problemset, classical-ml, model-evaluation]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Metrics & Evaluation'
topic: 'model evaluation'
hint: 'np.linspace edges; per bin average p and average y; last bin includes 1.0'
tools: [NumPy]
---

## Statement

Group predictions into equal-width probability bins on $[0,1]$ and compare, per bin, the average predicted probability with the observed rate of positives. `y` holds 0/1 labels and `p` the predicted probabilities. The last bin includes the value $1.0$; empty bins are skipped.

Implement `solve(y, p, bins=10)`.

**Returns.** Return a list of `(mean_confidence, observed_rate, count)` tuples, one for each non-empty bin in increasing order. `y` must be 0/1, `p` must lie in $[0,1]$ and both must have the same length; otherwise `ValueError` is raised.

### Examples

**Example 1**

Input:

```python
solve([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9], 2)
```

Output:

```text
[(0.15, 0.0, 2), (0.85, 1.0, 2)]
```

**Example 2**

Input:

```python
solve([0, 1, 0, 1], [0.1, 0.2, 0.8, 0.9], 2)
```

Output:

```text
[(0.15, 0.5, 2), (0.85, 0.5, 2)]
```

## Theory

### The simple version

A model is _calibrated_ if, among everything it labels "80% likely", about 80% turn out positive. Binning predictions and comparing the average prediction with the actual positive rate in each bin shows where it is over- or under-confident. These numbers are what a reliability diagram plots.

### The quantities

For bin $B$: $\text{confidence}=\frac1{|B|}\sum_{i\in B}p_i$ and $\text{rate}=\frac1{|B|}\sum_{i\in B}y_i$. A perfectly calibrated model has the two equal in every bin.

## Explanation

Bins are half-open $[a,b)$ except the last, which is closed so that $p=1.0$ is counted. The count per bin lets you ignore bins with very few points, whose rates are noisy. In the first example the model is slightly under-confident: its 0.15 bin has an observed rate of 0 and its 0.85 bin an observed rate of 1.
