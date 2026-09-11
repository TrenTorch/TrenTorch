---
name: linear-regression-hypothesis-function
title: Hypothesis Function
tags: [classical-ml, linear-regression, forward-pass]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Say you want to estimate something you can't measure directly — a house's price, a car's resale value, tomorrow's temperature — from a handful of things you _can_ measure: square footage, mileage, today's temperature. Each of those measurements probably matters a different amount. Square footage moves a house's price a lot; the color of the front door barely moves it at all. So the most basic possible estimator is: multiply each measurement by "how much it matters," add those up, and add one more number for "the baseline value before any measurement is even considered."

That's the entire problem. Nothing here is specific to neural networks or even to machine learning — it's the same idea as a weighted average, or a recipe where some ingredients count for more than others. What makes it worth a whole question is what comes next: doing this for many houses at once, and producing more than one estimate at a time (a real network layer rarely outputs just one number) — both without writing a single Python loop. Solve _that_ generalized version, and you've implemented `torch.nn.functional.linear`, the exact operation sitting inside every `nn.Linear` in every network you'll build in this curriculum.

### From theory to code

Theory below derives the one-row version: multiply each feature by its weight, sum them, add the bias. That's a dot product — `x · w`. Stack many rows into a matrix `X` and the same dot product repeated for every row _is_ matrix multiplication: `X @ w`. That's the whole leap from "the math" to "the code" for a single output.

The one piece that doesn't fall out automatically is handling more than one output at once. You're not computing one dot product per row anymore, you're computing `out_features` of them — one per row of `weight` (`weight`'s shape is `(out_features, in_features)`, so each of its rows is its own independent weight vector for one output). Lining `input` up against all of those rows simultaneously, in one matmul, is exactly what `weight.T` is for: `input @ weight.T` computes every output feature for every sample in a single expression, no loop over `out_features` either. Bias addition is the easy part — a plain `+` broadcasts a `(out_features,)` vector across every row for free.

Implement:

```python
def linear(
    input: np.ndarray,
    weight: np.ndarray,
    bias: np.ndarray | None = None,
) -> np.ndarray:
    """
    input:  shape (batch_size, in_features)
    weight: shape (out_features, in_features)
    bias:   shape (out_features,), or None

    Returns:
        output with shape (batch_size, out_features)
    """
```

### Constraints

- `input`: shape `(batch_size, in_features)`, `batch_size >= 1`, `in_features >= 1`.
- `weight`: shape `(out_features, in_features)`, `out_features >= 1` — matched to `input`'s `in_features`.
- `bias`: shape `(out_features,)`, or `None` — when `None`, no bias term is added at all, not a zero one.
- Output: shape `(batch_size, out_features)`, **always** — never squeezed to 1-D even when `out_features == 1`. Theory explains why that squeeze is a real bug, not a style choice.
- Output dtype matches `input`'s dtype exactly — no hardcoded `float32`/`float64` cast anywhere.
- One vectorized expression: no Python `for`/`while` loop over `batch_size` or `out_features`.
- `input`, `weight` and `bias` are never modified in place.

### Hints

1. **Get the transpose right before anything else.** `input` is `(batch_size, in_features)` and `weight` is `(out_features, in_features)` — the _same_ trailing dimension, so a plain `input @ weight` will straight-up crash for any non-square weight (and silently produce the wrong shape for a square one, which is worse). If your first attempt errors with a matmul shape mismatch, this is almost certainly why.
2. **Treat `bias=None` as a real branch, not an afterthought.** Don't default it to a zero array before the shape checks — check `bias is not None` and only add it then. Adding `None` to an array is a `TypeError`, and it's an easy one to miss if you only ever test with a real bias.
3. **Don't reach for `.reshape`, `.squeeze()`, or `.flatten()` anywhere in this function.** If you find yourself wanting one, it's a sign the shape is already wrong upstream — a correct implementation produces `(batch_size, out_features)` directly from `input @ weight.T (+ bias)`, with nothing left to reshape afterward.

## Theory

### The five-year-old version

Imagine you're guessing how much a used car costs. You don't just guess randomly — you look at things about the car (how old it is, how many miles it has driven, how many doors it has) and you weigh each thing in your head. "Every extra year knocks off about $800. Every 10,000 miles knocks off about $300. Doors don't matter much, maybe $50 each." Then you add up all those weighted guesses, plus some baseline starting price everyone begins at, and that's your final guess.

That's it. That's the whole idea. A _weight_ is "how much I care about this one feature." A _bias_ is "the number I'd guess even if every feature were zero." Multiply, add up, add the baseline. Done.

### The grown-up version

Formally, for one input row with features `x₁, x₂, ..., xₙ`, one weight per feature `w₁, w₂, ..., wₙ`, and a bias `b`, the prediction is:

```text
ŷ = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
```

This is called an **affine transformation** (linear, plus a shift). Written as a dot product between the feature vector `x` and the weight vector `w`, it becomes:

```text
ŷ = x · w + b
```

Now stack many rows of `x` into a matrix `X` (one row per sample) and the formula for the _entire batch at once_ becomes a single matrix multiplication:

```text
ŷ = Xw + b
```

`X @ w` relies on matrix multiplication doing, in one shot, exactly the "multiply each feature by its weight and sum" step for every row simultaneously. This is the entire reason vectorized code is both simpler _and_ faster than a Python loop: a `for` loop asks the CPU to do one multiply-add at a time; `X @ w` asks NumPy (and, underneath PyTorch, a GPU) to do all of them in parallel, using code written in C or CUDA instead of the Python interpreter.

### Why real PyTorch stores weight transposed

d2l.ai's own convention writes the single-output case as `ŷ = Xw + b`, with `w` as a plain feature vector — that's the cleanest way to _teach_ the idea, and it's what the theory above just did. But real `torch.nn.Linear` stores its weight as shape `(out_features, in_features)` and computes `input @ weight.T + bias`, not `input @ weight + bias`. Two reasons this isn't arbitrary:

- **Generality.** A real layer almost never has exactly one output. `nn.Linear(784, 128)` (a hidden layer in a small image classifier) has `out_features=128` — 128 independent weighted sums computed from the same input row, each with its own weight vector. Storing weight as `(out_features, in_features)` means _row `i` of weight_ is "the weight vector for output feature `i`", which stays true whether `out_features` is 1 or 1000. A plain `(in_features,)` vector only works for the special case of exactly one output — which is exactly what this question restricts itself to on the input side (single output), while still using the general shape convention so the function you write here is the same function a 128-output layer calls.
- **It composes.** Stack two of these (`linear` → some nonlinearity → `linear` again) and you have a two-layer neural network. Every layer in every architecture you'll ever build in this curriculum — CNNs, Transformers, all of it — bottoms out in calls to this exact operation with different `weight`/`bias` shapes plugged in. Get the shape convention right once, here, and it never has to be relearned.

### The shape gotcha that breaks real code

Because `weight` is `(out_features, in_features)`, the output is always `(batch_size, out_features)` — even when `out_features` happens to be 1. It is tempting to squeeze that trailing `1` away and return a flat `(batch_size,)` vector instead, since that's "obviously" what a single prediction per sample should look like.

Real PyTorch never does this, and there's a sharp reason why: NumPy and PyTorch both **broadcast** mismatched shapes instead of raising an error. If your prediction has shape `(batch_size, 1)` and you subtract a target vector of shape `(batch_size,)` from it — a completely ordinary thing to do when computing a loss — broadcasting silently expands both to `(batch_size, batch_size)` instead of raising a `ValueError` the way a shape mismatch "should." The result runs without crashing and produces a loss with the wrong value and the wrong gradient, with nothing in the traceback ever pointing at the real bug. This is one of the single most common real-world PyTorch bugs, and the fix starts here: never squeeze a dimension "because it looks nicer," only because the shape you're producing is genuinely, deliberately different from what the operation is supposed to return.

## Explanation

`input @ weight.T` relies on matmul broadcasting a `(batch_size, in_features)` array against a `(in_features, out_features)` one (`weight.T`) to produce `(batch_size, out_features)` directly — no reshape needed either side. Adding `bias`, shape `(out_features,)`, broadcasts it across every row of that result for free: NumPy lines up trailing dimensions, so a 1-D `(out_features,)` array adds itself to every row of a `(batch_size, out_features)` array without being told to.

`bias is not None` is checked explicitly rather than defaulting to a zero vector, matching what `torch.nn.functional.linear` actually does internally — `bias=None` is a real, first-class call students will make constantly once they reach normalization layers and residual blocks, where a following operation supplies its own shift and a redundant bias term would just be extra parameters learning to cancel each other out.

No dtype cast happens anywhere on purpose: whatever dtype `input` arrives in passes straight through matmul and addition unchanged, which is what "preserve dtype" in the requirements actually meant.
