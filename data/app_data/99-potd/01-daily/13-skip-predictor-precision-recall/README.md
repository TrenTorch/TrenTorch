---
name: potd-skip-predictor-precision-recall
title: 'THE SKIP PREDICTOR'
tags: [metrics-and-evaluation, classification]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Metrics & Evaluation, Classification

---

### Story

Spotify's skip-predictor flags tracks a listener is likely to abandon within 5 seconds. Before the
model is allowed near production traffic, it has to clear a basic precision/recall sanity check on
a held-out batch.

---

### The Math

```
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 * Precision * Recall / (Precision + Recall)
```

### Input Format

```
n
p_1 y_1
p_2 y_2
...
p_n y_n
```

`p_i` is the predicted binary label, `y_i` the true label, both `0` or `1`.

### Output Format

`precision recall f1`, space-separated, to 6 decimals.

### Constraints

- `1 <= n <= 10^6`
- Time limit: 1.0 second.

---

### Example

**Input**

```
8
1 1
1 0
0 0
1 1
0 0
0 1
1 1
0 0
```

**Output**

```
0.750000 0.750000 0.750000
```

**Explanation:** `TP = 3` (rows 1, 4, 7), `FP = 1` (row 2), `FN = 1` (row 6).
`P = 3/4 = 0.75`, `R = 3/4 = 0.75`, `F1 = 0.75`.

## Theory

### The simple version

Precision asks: of everything you flagged, how much did you get right? Recall asks: of everything that was actually true, how much did you catch? F1 is one number that punishes a model for ignoring either question.

### Both metrics can divide by zero

`TP + FP = 0` (no predicted positives) makes precision undefined by the formula, and
`TP + FN = 0` (no actual positives) makes recall undefined. This problem's convention: report
`0.000000` for that metric rather than crashing or returning `NaN`.

### F1 depends on both

Once precision and recall are computed (with the zero convention already applied), F1 follows the
harmonic-mean formula directly. If either precision or recall is `0`, F1 is `0` too (the harmonic
mean of anything with `0` is `0`).

### One pass is enough

`TP`, `FP`, and `FN` are each a simple count over the `n` rows. A single linear scan is all that is
needed; there is no reason to touch the data more than once even at `n = 10^6`.

## Explanation

`precision_recall_f1` counts `tp`, `fp`, and `fn` with vectorized boolean comparisons
(`(p == 1) & (y == 1)`, and so on), then applies the zero-division convention before dividing:
precision and recall are each `0.0` when their own denominator is `0`, computed _before_ the F1
formula is applied, so F1 never has to special-case anything itself, it just runs the harmonic-mean
formula on whatever precision and recall came out to.
