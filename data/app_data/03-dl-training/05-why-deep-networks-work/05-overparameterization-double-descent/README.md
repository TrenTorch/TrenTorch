---
name: dl-training-overparameterization-double-descent
title: 'Overparameterization and double descent: more parameters than data can still generalize'
tags: [neural-networks, theory, generalization]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Classical statistics has a well-known rule of thumb: a model with more parameters than training examples will OVERFIT catastrophically, perfectly memorizing the training set (including its noise) while generalizing terribly to new data. This intuition is genuinely correct for classical models, and it predicts that test error should get WORSE and worse as a model's parameter count approaches, and then exceeds, the number of training examples. Modern deep learning routinely violates this rule in a specific, reproducible, and genuinely surprising way: massively overparameterized networks (far more parameters than training examples, sometimes by many orders of magnitude) often generalize EXTREMELY well, frequently better than a "properly-sized," classically-recommended model would.

The "double descent" phenomenon (Belkin et al., 2019, building on earlier statistical learning theory) reconciles these two facts by showing that test error, plotted against parameter count, doesn't behave the way classical theory predicts (monotonically increasing once you cross the point where parameters equal training samples). Instead, it follows a genuine DOUBLE-DESCENT curve: test error decreases as parameters increase (as classical theory expects), then spikes sharply right around the "interpolation threshold" (where the model has JUST enough capacity to fit the training data exactly, and is forced to do so in a fragile, noise-sensitive way), and then, surprisingly, DECREASES again as parameters continue to grow well past that threshold, because a sufficiently overparameterized model has enough freedom to find a SMOOTH interpolating solution, not just any interpolating solution.

### From theory to code

Implement `build_features(x, weight, bias)` (the same sigmoid random-feature construction from `[01-universal-approximation]`, but taking an already-drawn `weight`/`bias` so the identical features can be applied to both a training set and a test set), `fit_min_norm(hidden, y)` (solve for output weights via `np.linalg.pinv`, the MINIMUM-NORM solution, essential once `num_features` exceeds the sample count and the system becomes underdetermined), and `train_and_test_mse(x_train, y_train, x_test, y_test, num_features, rng)`, which draws one shared random feature set, fits it on the training data, and reports both training and test MSE.

### Constraints

- `build_features` computes `sigmoid(np.outer(x, weight) + bias)`, taking `weight`/`bias` as arguments rather than drawing them itself.
- `fit_min_norm` must use `np.linalg.pinv`, not `np.linalg.lstsq`: the pseudoinverse specifically returns the MINIMUM-NORM solution in the overparameterized (underdetermined) case, which is the numerically well-behaved choice this whole demonstration depends on.
- `train_and_test_mse` must draw weight/bias ONCE and reuse the exact same values for both `build_features(x_train, ...)` and `build_features(x_test, ...)`, so training and test features live in the same space.
- Training MSE should reach essentially `0` once `num_features >= len(x_train)` (the interpolation threshold has been crossed).

### Hints

<details>
<summary>Hint 1</summary>

`build_features` is a one-liner: `sigmoid(np.outer(x, weight) + bias)`, identical to `[01-universal-approximation]`'s `random_hidden_features`, just with `weight`/`bias` passed in rather than generated internally.

</details>

<details>
<summary>Hint 2</summary>

`fit_min_norm(hidden, y) = np.linalg.pinv(hidden) @ y`. Unlike `np.linalg.lstsq`, which can behave ambiguously or error on some underdetermined systems, `np.linalg.pinv` always returns a well-defined result, and specifically the minimum-Euclidean-norm one when multiple exact solutions exist.

</details>

<details>
<summary>Hint 3</summary>

In `train_and_test_mse`: `weight = rng.randn(num_features); bias = rng.randn(num_features)`, drawn ONCE. Build `hidden_train` and `hidden_test` using those SAME `weight`/`bias` values (not two separate draws). Fit `output_weight` via `fit_min_norm(hidden_train, y_train)` (training data only), then compute both MSEs using `hidden_train @ output_weight` and `hidden_test @ output_weight` respectively.

</details>

## Theory

### The simple version

Picture fitting a curve through a small handful of noisy data points using a French curve template with adjustable knobs. With too FEW knobs, you can't bend the curve enough to get near every point (underfitting: high error everywhere). With EXACTLY enough knobs to touch every single point, the curve is forced into a uniquely determined, often wildly WIGGLY shape to hit each point precisely, since there's no slack left over (the interpolation threshold: the curve overfits badly, contorting itself around every bit of noise). With FAR MORE knobs than points, though, there are now countless different curves that all pass through every point exactly, and among all of them, the smoothest, least-wiggly one becomes an available and natural choice, so a sufficiently over-equipped tool can, counterintuitively, produce a SMOOTHER, better-generalizing fit than a tool with barely enough capacity to interpolate at all.

### The formula

There's no single closed-form formula for the double-descent curve's exact shape (it depends on the data distribution, the noise level, and the specific model class), but the mechanism this question demonstrates is:

```
train_and_test_mse(num_features):
    draw ONE random feature map (weight, bias) of size num_features
    hidden_train = build_features(x_train, weight, bias)
    hidden_test  = build_features(x_test,  weight, bias)
    output_weight = pinv(hidden_train) @ y_train      # minimum-norm fit
    train_mse = mse(hidden_train @ output_weight, y_train)
    test_mse  = mse(hidden_test  @ output_weight, y_test)
```

Sweeping `num_features` from well below the training set size to well above it and plotting `test_mse` traces the double-descent curve: `test_mse` falls, spikes sharply right around `num_features == len(x_train)` (the interpolation threshold), and falls again for `num_features` well beyond it.

### How PyTorch actually implements this

There's no PyTorch API for "double descent" itself (like `[01-universal-approximation]`, this is a theoretical/empirical phenomenon, not a specific function), but the phenomenon is directly why training a MUCH larger neural network than "seems necessary" for a given dataset size has become completely standard practice in deep learning, rather than the cautious, capacity-matched approach classical statistics would recommend. Real neural networks trained with gradient descent (rather than `fit_min_norm`'s explicit minimum-norm closed-form solve) show the same qualitative double-descent behavior for a related reason: gradient descent, started from small random initial weights, has its own implicit bias toward finding relatively SMOOTH, low-norm solutions among the many that fit the training data exactly, closely mirroring what `np.linalg.pinv`'s explicit minimum-norm solve does here directly and in closed form. This is part of why modern practice increasingly favors "scale up the model, not just the data" (directly connected to `Note: scaling laws, why bigger models trained on more data reliably get better`, immediately following this question): a sufficiently large model isn't just tolerating overparameterization, it's actively benefiting from the smoother interpolating solutions that extra capacity makes available.

## Explanation

`build_features` computes `sigmoid(np.outer(x, weight) + bias)` directly, identical in shape to `[01-universal-approximation]`'s hidden-layer construction, but accepting `weight`/`bias` as arguments so the SAME random feature map can be evaluated on two different input sets.

`fit_min_norm` returns `np.linalg.pinv(hidden) @ y`: the pseudoinverse-based solve, which reduces to ordinary least squares when `hidden` has more rows than columns (underparameterized), and returns the minimum-Euclidean-norm exact interpolating solution when `hidden` has more columns than rows (overparameterized), giving a single, well-defined formula that correctly spans both regimes.

`train_and_test_mse` draws `weight`/`bias` once via `rng`, builds `hidden_train` and `hidden_test` from that SAME shared random feature map, fits `output_weight` using only the training features and targets via `fit_min_norm`, and computes both MSEs by applying that one `output_weight` to each set's own hidden features, letting the same fitted model's train and test performance be compared directly across different values of `num_features`.
