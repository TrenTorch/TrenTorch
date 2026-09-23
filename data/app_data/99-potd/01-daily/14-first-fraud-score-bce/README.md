---
name: potd-first-fraud-score-bce
title: 'THE FIRST FRAUD SCORE'
tags: [loss-functions]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Loss Functions

---

### Story

PayPal's very first fraud model outputs a raw probability per transaction. Before anyone trusts the
model, its loss on a labeled calibration batch needs to be computed exactly, matching the framework
reference to the last digit.

---

### The Math

```
L = -(1/n) * sum_i [ y_i * log(yhat_i) + (1 - y_i) * log(1 - yhat_i) ]
```

### Input Format

```
n
y_1 yhat_1
...
y_n yhat_n
```

### Output Format

Scalar loss, 6 decimals.

### Constraints

- `1 <= n <= 10^5`, `10^-7 <= yhat_i <= 1 - 10^-7`
- Time limit: 1.0 second.

---

### Example

**Input**

```
4
1 0.9
0 0.2
1 0.6
0 0.3
```

**Output**

```
0.299001
```

## Theory

### The simple version

Cross-entropy loss rewards a model for being confidently right and punishes it heavily for being confidently wrong. A 0.9 prediction on a true label costs very little; a 0.1 prediction on that same true label costs a lot.

### The input is already clamped

The constraints guarantee `yhat_i` never touches exactly `0` or `1`, so no additional
epsilon-clamping is needed inside the solution. Adding an extra clamp on top of an already-safe
input would only ever change the answer, never protect it.

### Every row contributes exactly one term

Each row's true label picks out exactly one of the two terms in the sum: when `y_i = 1`, only
`log(yhat_i)` matters and `(1 - y_i)` is `0`, wiping out the other term. When `y_i = 0`, it is the
reverse. Forgetting that the `(1 - y_i)` term evaluates to exactly `0` (rather than skipping it) is
the classic way to accidentally add a stray term to an all-one-class batch.

### Vectorize the sum

At `n = 10^5`, a per-row Python loop calling `math.log` twice per row is slow enough to matter on an
interpreted reference; a single vectorized `np.log` call over the whole batch avoids that.

## Explanation

`bce_loss` computes both log terms for the whole batch at once with `np.log(yhat)` and
`np.log(1 - yhat)`, combines them as `y * log(yhat) + (1 - y) * log(1 - yhat)`, and returns the
negative mean over all `n` rows. Because `y` is `0` or `1`, the two terms of the sum are mutually
exclusive per row without any branching: `y` and `(1 - y)` do the selection arithmetically.
