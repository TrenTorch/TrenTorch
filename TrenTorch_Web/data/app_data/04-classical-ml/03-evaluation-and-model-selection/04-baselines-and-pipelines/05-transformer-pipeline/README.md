---
name: evaluation-transformer-pipeline
title: Transformer pipeline
tags: [classical-ml, evaluation, pipelines, data-leakage]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Standard scaler without leakage` showed why preprocessing must learn its statistics from training data only. Real projects chain several preprocessing steps, and doing that by hand invites mistakes. A pipeline bundles the steps in order: fitting the pipeline fits each step on the output of the previous one, and transforming new data replays the same sequence with the fitted numbers.

Implement two classes.

- `MinMaxScaler`: `fit(X)` stores each column's minimum and maximum. `transform(X)` returns `(X - min) / (max - min)`. A column whose training range is zero maps every value to `0`. `fit_transform(X)` fits, then transforms `X`, and returns the result.
- `Pipeline(steps)`: `steps` is a list of transformers. `fit_transform(X)` runs each step's `fit_transform` in order and returns the final output. `transform(X)` runs each step's `transform` in order.

### Constraints

- `transform` never refits anything. Values outside the training range may fall outside `[0, 1]`, and that is correct.
- `fit` returns the scaler itself, so calls can be chained.
- Do not modify the inputs.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

For a zero range, divide by `np.inf` instead of zero: finite values divided by infinity become zero, with no warnings.

</details>

<details>
<summary>Hint 2</summary>

In `Pipeline.fit_transform`, reassign `X` at each step: `X = step.fit_transform(X)`.

</details>

## Theory

### The simple version

A pipeline is a conveyor belt. Each station does one job, and the belt carries the output of one station into the next. Fitting happens station by station, so every station learns from data that has already been prepared the way it will see it at prediction time.

### The formula

For a column with training minimum $m$ and maximum $M$:

$$
x' = \frac{x - m}{M - m}, \qquad x' = 0 \text{ when } M = m
$$

## Explanation

`MinMaxScaler.fit` records the column minima and maxima. `transform` divides by the range, using infinity for zero ranges so those columns become zero. `Pipeline` holds the steps in a list and passes data through them in order, using `fit_transform` while fitting and `transform` afterward.
