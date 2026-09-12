---
name: dl-training-universal-approximation
title: 'Universal approximation: why one wide hidden layer can fit any function, in principle'
tags: [neural-networks, theory]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A striking, genuinely surprising mathematical fact underlies everything else in this curriculum: a neural network with just ONE hidden layer, no depth at all, can approximate essentially any reasonable function to arbitrary precision, given enough hidden units. This is the Universal Approximation Theorem (Cybenko, 1989; Hornik, 1991), and it's worth sitting with why it's surprising: `[02-layers/01-linear-forward]`'s `linear_forward` on its own can only ever represent a STRAIGHT LINE (or a flat hyperplane, in higher dimensions), no matter how you set its weights. Stack a nonlinearity (like `sigmoid`, used here) between two linear layers, though, and each hidden unit becomes a smoothly-adjustable "bump" or "step" that can be placed, scaled, and combined with every other hidden unit's own bump, and a large enough COLLECTION of these adjustable bumps can be combined to approximate arbitrarily complex curves.

The theorem is an EXISTENCE proof, not a practical training recipe: it says a wide-enough network with the right weights exists, not that gradient descent will easily find those weights, or that "wide and shallow" is actually a good architecture in practice (it usually isn't; `Representation learning: why depth learns hierarchical features, not one big lookup`, immediately following this question, is exactly about why DEPTH, not just width, tends to work much better in practice). This question demonstrates the existence claim directly and numerically: build a wide hidden layer with RANDOM (untrained) weights, and show that simply choosing the right OUTPUT layer weights (a cheap, closed-form least-squares fit, no gradient descent needed) is enough to approximate a genuinely nonlinear target function, and that approximation gets dramatically better as the hidden layer gets WIDER.

### From theory to code

Implement `random_hidden_features(x, num_hidden, rng)`, `fit_output_weights(hidden, y)`, and `approximate_function(x, y, num_hidden, rng)`. `random_hidden_features` builds `num_hidden` sigmoid neurons, each with its own RANDOM weight and bias (already generated for you, `weight = rng.randn(num_hidden) * 5.0` and similarly for `bias`), applied to every point in `x`, producing a `(len(x), num_hidden)` matrix. `fit_output_weights` solves, via `np.linalg.lstsq`, for the linear combination of those hidden-layer columns that best matches target `y`. `approximate_function` ties both together and reports the mean squared error of the fit.

### Constraints

- `random_hidden_features` must return a matrix of shape `(len(x), num_hidden)`: one column per hidden neuron, applying THAT neuron's own weight and bias to every point in `x`.
- `fit_output_weights` must use `np.linalg.lstsq(hidden, y, rcond=None)` (least squares), not gradient descent, this is a closed-form, exact best fit given the FIXED (untrained) hidden layer.
- `approximate_function` must reuse both functions above rather than reimplementing their logic.
- The returned `mse` should decrease substantially as `num_hidden` increases, for the same target function, demonstrating the "wider approximates better" intuition.

### Hints

<details>
<summary>Hint 1: random_hidden_features</summary>

`np.outer(x, weight)` produces a `(len(x), num_hidden)` matrix where entry `[i, j]` is `x[i] * weight[j]`; adding `bias` (broadcasting across rows) and applying `sigmoid` gives the full hidden layer activation matrix in one line: `sigmoid(np.outer(x, weight) + bias)`.

</details>

<details>
<summary>Hint 2: fit_output_weights</summary>

`np.linalg.lstsq(hidden, y, rcond=None)` returns a tuple whose FIRST element is the least-squares solution; unpack it with `weight, *_ = np.linalg.lstsq(hidden, y, rcond=None)` (the `*_` discards the other returned diagnostics: residuals, rank, singular values, which aren't needed here).

</details>

<details>
<summary>Hint 3: approximate_function</summary>

Call `random_hidden_features` to get `hidden`, call `fit_output_weights(hidden, y)` to get the output weights, compute `pred = hidden @ output_weight`, and `mse = mean((pred - y)^2)`.

</details>

## Theory

### The simple version

Approximating a curvy coastline on a map using only a large enough collection of small straight rulers laid end to end: no single ruler can bend, but with ENOUGH short rulers, each placed and angled just right, the overall zigzag path can trace an arbitrarily close approximation to any coastline, no matter how curvy. A sigmoid hidden unit is a "soft" version of one of those rulers, a smooth S-shaped step that can be positioned (via its bias) and scaled (via its weight) anywhere along the input axis; combining enough of them, each contributing its own small S-shaped correction, approximates arbitrarily complex curves.

### The formula

For a single-hidden-layer network with `num_hidden` sigmoid units, approximating a function `f`:

```
hidden_j(x) = sigmoid(weight_j * x + bias_j)          for each hidden unit j
output(x)   = sum over j of (output_weight_j * hidden_j(x))
```

The Universal Approximation Theorem states: for any continuous function `f` on a bounded domain, and any tolerance `epsilon > 0`, there EXIST values of `num_hidden`, `weight`, `bias`, and `output_weight` such that `|output(x) - f(x)| < epsilon` for every `x` in the domain. This question fixes `weight`/`bias` at RANDOM values (rather than searching for the theoretically optimal ones) and solves only for `output_weight`, which is enough to demonstrate the same qualitative effect: more hidden units, better approximation, even without any search over the hidden layer's own parameters at all.

### How PyTorch actually implements this

Nothing in PyTorch computes "the" universal approximation directly, this question's random-features approach (fixed random hidden weights, solved-for output weights) is closer to a classical technique called the "Extreme Learning Machine" or, more broadly, "random feature methods" (also connected to kernel methods: an infinitely-wide random-feature layer with the right random weight DISTRIBUTION converges to a specific kernel, the exact idea explored more deeply in `Note: neural tangent kernel, an infinitely-wide network behaves like a fixed kernel`, later in this track) than to how real networks are actually trained. In practice, EVERY layer's weights, hidden included, are trained jointly via gradient descent (`[03-training-loop/02-assemble-training-loop]`'s full loop), which in practice finds MUCH more efficient, useful representations than random hidden features ever could, learning hidden units that respond to genuinely meaningful patterns in the data rather than firing at arbitrary, randomly-placed locations. The theorem's real, practical message isn't "use one wide layer," it's the reassurance that a large enough neural network is never fundamentally too SIMPLE a model class to represent whatever the true underlying function is, if training struggles, the problem is virtually always the optimization (finding good weights) or generalization (avoiding overfitting), never the network's raw representational capacity.

## Explanation

`random_hidden_features` computes `sigmoid(np.outer(x, weight) + bias)`: `np.outer(x, weight)` produces every `x[i] * weight[j]` pairing as a `(len(x), num_hidden)` matrix in one call, and adding `bias` (broadcast across every row) then applying `sigmoid` produces the full hidden activation matrix, one column per (randomly parameterized) hidden neuron.

`fit_output_weights` calls `np.linalg.lstsq(hidden, y, rcond=None)` and unpacks its first return value, the exact least-squares solution for the linear output weights that best reconstruct `y` from the fixed hidden-layer activations.

`approximate_function` chains both: builds `hidden` via `random_hidden_features`, solves for `output_weight` via `fit_output_weights`, computes `pred = hidden @ output_weight`, and returns `(pred, mean squared error of pred vs y)`, directly measuring how well the fit approximates the target function.
