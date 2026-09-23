---
name: potd-eta-scorecard-mae
title: 'THE ETA SCORECARD'
tags: [metrics-and-evaluation]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Metrics & Evaluation

---

### Story

Uber's ETA team tracks one north-star error number every single day: simple, but it has to be
exactly right, since it's the number that goes in front of leadership.

---

### The Math

```
MAE = (1/n) * sum_i |y_i - yhat_i|
```

### Input Format

```
n
y_1 yhat_1
...
y_n yhat_n
```

### Output Format

Scalar MAE, 6 decimals.

### Constraints

- `1 <= n <= 10^6`
- Time limit: 1.0 second.

---

### Example

**Input**

```
4
10 12
15 14
20 18
12 13
```

**Output**

```
1.500000
```

## Theory

### The simple version

Mean absolute error answers one plain question: on average, how many minutes (or dollars, or whatever the units are) was the prediction off by, regardless of which direction it missed in?

### Sign does not matter, magnitude does

ETA-delta features (and the errors on them) can be negative in either direction: the model can
predict early or late. The absolute value must apply to `(y_i - yhat_i)` regardless of which side
it lands on; a mistake that only handles one sign of error will pass an all-one-direction test batch
and fail a mixed one.

### All-zero error is a real answer

If every prediction matches its label exactly, MAE is exactly `0.000000`, not a sign of a bug in the
metric itself.

### One pass, no intermediate array

At `n = 10^6`, materializing an intermediate list of absolute errors before summing wastes memory
for no benefit; a single running (or vectorized) sum is all this needs.

## Explanation

`mae` computes `np.abs(y - yhat)` once over the whole batch and returns its mean. Vectorizing both
the subtraction and the absolute value means the sign of any individual error never needs to be
inspected by hand: NumPy's `abs` already handles positive and negative differences uniformly, so a
batch of errors in both directions is no different from a batch that all point the same way.
