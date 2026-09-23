---
name: potd-cancellation-sanity-check-accuracy
title: 'CANCELLATION SANITY CHECK'
tags: [metrics-and-evaluation]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Metrics & Evaluation

---

### Story

A first-pass cancellation classifier needs one sanity-check number before the team invests in
anything more sophisticated than accuracy.

---

### The Math

```
Accuracy = (TP + TN) / n
```

### Input Format

```
n
p_1 y_1
...
p_n y_n
```

### Output Format

Scalar accuracy, 6 decimals.

### Constraints

- `1 <= n <= 10^6`
- Time limit: 1.0 second.

---

### Example

**Input**

```
6
1 1
0 0
1 0
1 1
0 0
0 1
```

**Output**

```
0.666667
```

## Theory

### The simple version

Accuracy is the simplest possible score there is: out of everything predicted, what fraction did the model get right?

### Accuracy is just agreement

`TP + TN` is simply the count of rows where the prediction equals the label; there is no need to
compute `TP` and `TN` separately and add them, comparing `p_i == y_i` directly gives the same count
in one pass.

### The two extremes are exact

All predictions correct gives accuracy exactly `1.000000`; all predictions wrong gives exactly
`0.000000`. Both are useful sanity checks on the formula itself, not edge cases requiring special
handling.

### The simplest metric in this set

This is deliberately the baseline metric, included as much as a smoke test of I/O throughput at
`n = 10^6` as a check of the formula. A single vectorized comparison and mean is all it needs.

## Explanation

`accuracy` computes `(p == y).mean()` directly: a boolean array where `p_i == y_i` is exactly the
set of rows counted in `TP + TN` combined (a correct row is either a true positive or a true
negative, and every incorrect row is a false positive or false negative, neither counted), so its
mean over `n` rows is the accuracy formula in one vectorized expression, with no separate `TP`/`TN`
bookkeeping required.
