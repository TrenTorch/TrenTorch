---
name: linear-regression-hypothesis-function
title: Hypothesis Function
tags: [classical-ml, linear-regression, forward-pass]
difficulty: Beginner
---

## Statement

Every layer in a real neural network is built out of one operation, repeated with different numbers plugged in. The first thing that touches your input in a Transformer's feed-forward block, the last layer that turns hidden features into logits, every `nn.Linear` you will ever write: all of them are this one operation. PyTorch calls it `torch.nn.functional.linear`, and it is what you are about to implement.

Given a batch of input rows and a layer's weight matrix and bias vector, produce one output row per input row. This is also, not coincidentally, exactly what a linear regression model computes — the same operation, doing double duty as a whole model instead of one piece of a bigger one.

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

Your function should:

1. Match `torch.nn.functional.linear`'s real signature and shape convention exactly — `weight` is `(out_features, in_features)`, not the other way around, because that is how PyTorch actually stores every `nn.Linear`'s weight matrix.
2. Support `bias=None` (no bias term) as well as a real bias vector, the same as PyTorch does.
3. Compute the whole batch in a single vectorized expression — no Python `for` loop over samples.
4. Preserve `input`'s dtype in the output (don't hardcode `float32`/`float64`).
5. Never squeeze the output. `out_features=1` still returns shape `(batch_size, 1)`, not `(batch_size,)` — this is deliberate, and Theory explains why it matters.

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
