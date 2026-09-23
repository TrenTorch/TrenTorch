---
name: potd-stockout-threshold-sweep-f1
title: 'STOCKOUT THRESHOLD SWEEP'
tags: [classification, metrics-and-evaluation]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Classification, Metrics & Evaluation

---

### Story

Walmart's stockout classifier ships with a default 0.5 decision threshold, but the business cost of
a missed stockout versus a false alarm isn't symmetric, so the team wants the threshold that
actually maximizes F1 on their validation set, not the framework default.

---

### The Math

For each distinct score value `t` present in the data, using `t` as the decision threshold (predict
positive if `score >= t`), compute `F1(t)`; return the `t` maximizing `F1` (ties broken by the
**larger** threshold).

### Input Format

```
n
score_1 y_1
...
score_n y_n
```

### Output Format

`best_threshold best_f1`, 6 decimals.

### Constraints

- `1 <= n <= 10^5`
- Time limit: 1.0 second.

---

### Example

**Input**

```
8
0.9 1
0.8 1
0.75 0
0.6 1
0.55 0
0.4 0
0.3 1
0.2 0
```

**Output**

```
0.600000 0.750000
```

## Theory

### The simple version

A classifier hands you a score, not a decision, until you pick a cutoff. This tries every possible cutoff and reports the one that gives the best balance of precision and recall.

### Ties go to the more conservative threshold

When multiple thresholds tie for the best F1, the answer is the **largest** among them: a stated,
deliberate convention, the more conservative operating point (flags fewer things positive at the
same F1). This must be explicit, since "the best threshold" is otherwise ambiguous at a tie.

### An undefined F1 never wins

At some thresholds, precision or recall's own denominator can be `0` (no predicted positives, or no
actual positives among the ones scored above threshold). That threshold's F1 is undefined and must
never be allowed to win the max, regardless of how the undefined value is represented internally.

### Sweep once, don't recompute from scratch

Recomputing `TP`/`FP`/`FN` from the full dataset for every one of up to `n` candidate thresholds is
`O(n^2)` and too slow at `n = 10^5` with many duplicate scores. Sort once by score descending, then
sweep the threshold downward while maintaining running `TP`/`FP` counts, an `O(n log n)` solution.

## Explanation

`best_f1_threshold` sorts rows by score descending, then walks them once, incrementally updating
running `TP` and `FP` counts as each row's score is included at or above the current threshold. It
evaluates `F1` only at the distinct score values (grouping rows that share a score, since the
prediction only changes when the threshold crosses to a new distinct value), skips a threshold
whose precision or recall denominator is `0`, and keeps the first (largest) threshold it sees for
the current best `F1`, only replacing it when a later, smaller threshold's `F1` is strictly greater,
never on a tie. Sweeping downward through distinct thresholds and updating counts incrementally,
rather than rescanning the whole dataset per threshold, is what keeps this `O(n log n)`.
