---
name: evaluation-validation-curves
title: 'Validation curves: training/validation error vs. one hyperparameter'
tags: [classical-ml, evaluation, model-complexity]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`08-learning-curves` fixed the model and swept the _amount of data_ to ask "would more data help?" There's a second, equally natural question: fixing the amount of data, how does one hyperparameter, polynomial degree, tree depth, number of estimators, actually trade off underfitting against overfitting for this dataset? `03-bias-variance-tradeoff` explained that tradeoff in the abstract; a validation curve makes it visible for one real, tunable number at a time.

This matters beyond curiosity: `04-grid-search` and `05-random-search` already search over hyperparameters automatically, but they hand back a single winning value with no visibility into _why_ it won, or how sensitive the result is to picking a slightly different one. A validation curve is the same search made visible, one hyperparameter, plotted.

### From theory to code

Theory describes the expected shape: training error trending down as complexity increases, validation error tracing a U, dropping, bottoming out, then climbing again as the model starts overfitting the fixed training set.

Producing that curve needs the same mechanical step at every candidate value: train on the same fixed data with that one hyperparameter setting, measure both errors, record them. Implement `validation_curve(fit_and_evaluate_fn, param_values)`, which owns exactly that sweep; the caller-supplied `fit_and_evaluate_fn` does the actual training and measuring.

### Constraints

- `fit_and_evaluate_fn(param_value) -> (train_error, val_error)`: trains a model with this one hyperparameter value, against the same, fixed training set every call, and returns both errors.
- `param_values`: a list of values (numbers, or anything `fit_and_evaluate_fn` accepts), not necessarily sorted.
- Call `fit_and_evaluate_fn` exactly once per entry in `param_values`, in the order given.
- Returns `(train_errors, val_errors)`, each shape `(len(param_values),)`, in the same order as `param_values`.
- Do not swap which returned value goes into which output array.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Structurally this is the exact same sweep as `08-learning-curves`'s `learning_curve`, only what varies between calls is different, a hyperparameter value here instead of a training-set size.

</details>

<details>
<summary>Hint 2</summary>

Keep two plain Python lists while looping over `param_values`, appending the unpacked `(train_error, val_error)` tuple each time, then wrap both in `np.array` right before returning.

</details>

## Theory

### The simple version

Think of tuning the amount of seasoning in a recipe. Too little (low complexity), and the dish tastes bland to everyone, including you, the cook, tasting your own batch (both training and validation error high). Add more, and it tastes better to you and to guests alike, up to a point. Add too much, and you (the cook, tasting the exact batch you seasoned) might still say it's fine, but guests (validation) start complaining, you've over-fit the seasoning to your own palate. A validation curve is that same experiment, plotted across "how much seasoning" instead of tasted by hand.

### The formula

```text
for param_value in param_values:
    train_error, val_error = fit_and_evaluate_fn(param_value)
    record train_error into train_errors
    record val_error into val_errors
return train_errors, val_errors
```

Reading the resulting arrays against complexity:

```text
error
  |  val: high \                    / high (overfitting climbs back up)
  |          \                    /
  |           \___low (sweet spot, the U's bottom)
  |  train:          \___________________ (keeps dropping)
  +-------------------------------------------- complexity →
```

`train_errors` trends down (not necessarily strictly monotonic) as complexity rises. `val_errors` has a minimum strictly between the two extremes, `argmin(val_errors)` is neither the first nor the last index, and `val_errors` at the highest complexity is worse than at that minimum.

### How PyTorch actually implements this

There's no single `torch` function for this either, it's an evaluation protocol layered on top of an ordinary training loop, the same one `01-linear-regression/05-training-loop` builds. In practice this loop retrains a fresh model (or fresh tree/ensemble) once per candidate hyperparameter value on the same fixed `train_input`/`train_labels`, records the training loss and a separate validation-set loss for each, exactly the shape `fit_and_evaluate_fn` is expected to have here.

## Explanation

`validation_curve` in `solution.py` is structurally identical to `08-learning-curves`'s `learning_curve`: it initializes `train_errors = []` and `val_errors = []`, loops over `param_values`, and for each `param_value` calls `train_error, val_error = fit_and_evaluate_fn(param_value)`, appending each to its list before returning `np.array(train_errors), np.array(val_errors)`. The only difference from `08-learning-curves` is what varies between calls, a hyperparameter value here, a training-set size there, both leave the actual training and evaluation entirely to the caller-supplied function; `tests.py`'s `test_calls_fit_and_evaluate_once_per_param_value` and `test_shows_the_classic_u_shape_against_polynomial_degree` confirm this loop does nothing beyond the sweep, and that a real fixed-data, varying-degree fit (via `03-bias-variance-tradeoff`'s `fit_polynomial`/`predict_polynomial`) actually produces the U-shape Theory describes, with `argmin(val_errors)` landing strictly inside `degrees`, not at either end.
