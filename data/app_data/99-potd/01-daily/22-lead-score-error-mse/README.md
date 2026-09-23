---
name: potd-lead-score-error-mse
title: 'LEAD SCORE ERROR'
tags: [loss-functions]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Loss Functions

---

### Story

A lead-scoring regressor is graded against actual conversion likelihood using the most standard
regression loss there is, but it has to match the framework reference exactly before it ships into
the training loop.

---

### The Math

```
MSE = (1/n) * sum_i (y_i - yhat_i)^2
```

### Input Format

```
n
y_1 yhat_1
...
y_n yhat_n
```

### Output Format

Scalar MSE, 6 decimals.

### Constraints

- `1 <= n <= 10^6`
- Time limit: 1.0 second.

---

### Example

**Input**

```
4
3 2.5
5 5
2.5 4
7 8
```

**Output**

```
0.875000
```

## Theory

### The simple version

Mean squared error punishes big mistakes much more than small ones, because each error is squared before it is averaged. A model that is off by 10 pays four times the penalty of one that is off by 5, not just twice.

### Square each error first, then average

The squaring happens per row, before the average: `mean((y - yhat)^2)`, not
`mean(y - yhat)^2`. Averaging the raw errors first (which can cancel positive and negative errors
against each other) and squaring the result afterward gives a completely different, much smaller
number whenever errors point in both directions.

### Outliers dominate on purpose

A handful of rows with very large errors contribute disproportionately to MSE, because the error is
squared before averaging. That is expected behavior for this metric, not a bug to guard against.

### One pass, vectorized

At `n = 10^6`, a single vectorized `(y - yhat) ** 2` followed by `.mean()` avoids both a Python loop
and any unnecessary intermediate list.

## Explanation

`mse` computes `diff = y - yhat` once, squares it elementwise with `diff ** 2`, and returns the mean
over the whole batch. Squaring happens before the reduction, which is what keeps positive and
negative errors from canceling: two rows with errors `+2` and `-2` contribute `4` and `4` to the
mean, not `0`, exactly the behavior the "square then average" order guarantees.
