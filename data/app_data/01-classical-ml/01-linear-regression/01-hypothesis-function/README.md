---
name: linear-regression-hypothesis-function
title: Hypothesis Function
tags: [classical-ml, linear-regression, forward-pass]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Say you want to estimate a house's price from things you can measure: square footage, mileage on the neighborhood, today's temperature. Each measurement matters a different amount. So the simplest possible estimator is: multiply each measurement by "how much it matters," add those up, then add one more number for the baseline value before any measurement counts.

That's the whole problem, and it has nothing to do with neural networks yet. What makes it worth a question is doing this for many houses at once, and for more than one estimate at a time, without a Python loop. Solve that, and you've implemented `torch.nn.functional.linear`: the operation inside every `nn.Linear` you'll build in this curriculum.

### From theory to code

Theory derives the one-row version: multiply each feature by its weight, sum them, add the bias. That's a dot product, `x · w`. Stack rows into a matrix `X` and the same dot product repeated per row is matrix multiplication: `X @ w`.

The one thing that doesn't fall out automatically is more than one output. `weight` has shape `(out_features, in_features)`, so each of its rows is its own independent weight vector. `input @ weight.T` lines `input` up against every one of those rows at once, computing every output feature for every sample in a single expression.

Implement `linear(input, weight, bias=None)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `input`: shape `(batch_size, in_features)`.
- `weight`: shape `(out_features, in_features)`.
- `bias`: shape `(out_features,)`, or `None` (no bias term added, not a zero one).
- Output: shape `(batch_size, out_features)`, always, never squeezed. Theory explains why.
- Output dtype matches `input`'s dtype exactly.
- One vectorized expression, no loop over `batch_size` or `out_features`.
- `input`, `weight` and `bias` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`input` and `weight` share their last dimension, not their first. Which one needs transposing before a matmul lines up?

</details>

<details>
<summary>Hint 2</summary>

`bias=None` is a real branch, not a default-to-zero. Adding `None` to an array raises a `TypeError`. Check `bias is not None` first.

</details>

<details>
<summary>Hint 3</summary>

If you reach for `.reshape`, `.squeeze()`, or `.flatten()` anywhere here, stop. A correct implementation produces the right shape directly from `input @ weight.T (+ bias)`.

</details>

## Theory

### The simple version

Imagine guessing a used car's price. You look at things about it (age, mileage, doors) and weigh each one in your head: "every extra year knocks off about $800, every 10,000 miles about $300, doors barely matter." Add up the weighted guesses, plus a baseline starting price, and that's your final guess.

That's the whole idea. A weight is how much you care about one feature. A bias is the number you'd guess even with every feature at zero.

### The formula

For one row with features `x₁, x₂, ..., xₙ`, weights `w₁, w₂, ..., wₙ`, and bias `b`:

```text
ŷ = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
```

This is an affine transformation: linear, plus a shift. As a dot product:

```text
ŷ = x · w + b
```

Stack many rows into a matrix `X` and the whole batch becomes one matrix multiplication:

```text
ŷ = Xw + b
```

`X @ w` does the "multiply each feature by its weight, sum" step for every row at once. That's why vectorized code is both simpler and faster than a loop: NumPy (and, underneath PyTorch, a GPU) runs all the multiply-adds in parallel, in C or CUDA, instead of one at a time in the Python interpreter.

### Why PyTorch stores weight transposed

d2l.ai's convention writes this as `ŷ = Xw + b`, with `w` a plain feature vector. That's the clearest way to teach the idea. Real `torch.nn.Linear` instead stores weight as `(out_features, in_features)` and computes `input @ weight.T + bias`. Two reasons:

- **Generality.** A real layer rarely has one output. `nn.Linear(784, 128)` needs 128 independent weighted sums from the same input row, one per weight-matrix row. `(out_features, in_features)` stays correct whether `out_features` is 1 or 1000; a plain `(in_features,)` vector only covers the special case of exactly one output.
- **It composes.** Stack `linear`, a nonlinearity, `linear` again, and you have a two-layer network. Every architecture in this curriculum bottoms out in this same operation with different `weight`/`bias` shapes plugged in. Get the convention right once and it never needs relearning.

### The shape gotcha that breaks real code

Because output is `(batch_size, out_features)` even when `out_features` is 1, it's tempting to squeeze that trailing `1` away into a flat `(batch_size,)` vector.

Real PyTorch never does. NumPy and PyTorch broadcast mismatched shapes instead of raising an error: subtract a `(batch_size,)` target from a `(batch_size, 1)` prediction (an ordinary step in computing a loss) and both silently expand to `(batch_size, batch_size)`, no `ValueError`, no crash, just a loss with the wrong value and the wrong gradient. Nothing in the traceback points at the real bug. This is one of the most common real PyTorch mistakes: never squeeze a dimension because it "looks nicer," only when the shape is genuinely, deliberately different. (The next question, MSE Loss, is exactly where this bites.)

### How PyTorch actually implements this

`torch.nn.functional.linear` isn't Python doing `input @ weight.T + bias` under the hood. It's a thin wrapper around a fused ATen kernel (`aten::linear`), C++ that dispatches to an optimized matrix-multiply routine (BLAS on CPU, cuBLAS on GPU) and knows how to compute its own gradient directly, instead of chaining a matmul op's gradient with a separate add op's gradient. Same math, faster, and one gradient formula instead of two stitched together.

`torch.nn.Linear` is the module you'll actually write in real code: `nn.Linear(in_features, out_features, bias=True, device=None, dtype=None)`. A few things worth knowing about it:

- `self.weight` and `self.bias` are `nn.Parameter` tensors, not plain arrays. That's what makes an optimizer able to find and update them automatically, and what makes `.requires_grad` track them through autograd.
- `bias=True` is a construction-time choice, not a per-call one. Set it once and the layer either always has a bias or never does. The `bias=None` you implemented here is the per-call version of the same idea, `F.linear` gets called either way, with or without one.
- Weights aren't zero-initialized like this question's downstream training loop starts them. Real `nn.Linear` initializes `weight` with Kaiming-uniform and `bias` with a uniform range based on `in_features`, specifically so a freshly-created network's activations don't explode or vanish before any training happens.
- `input` isn't restricted to 2-D in real PyTorch. `F.linear` accepts any number of leading batch dimensions, `(*, in_features)` for any `*`, and only ever transforms the last one. This question restricts you to the 2-D case because that's the shape every other question in this track needs, but the same function you wrote here generalizes for free once you understand why the last dimension is the one that matters.

## Explanation

`input @ weight.T` broadcasts `(batch_size, in_features)` against `weight.T`'s `(in_features, out_features)` to produce `(batch_size, out_features)` directly, no reshape either side. Adding `bias`, shape `(out_features,)`, broadcasts it across every row for free: NumPy lines up trailing dimensions.

`bias is not None` is checked explicitly instead of defaulting to a zero vector, matching what `torch.nn.functional.linear` does internally. `bias=None` is a call students will make constantly once they reach normalization layers and residual blocks, where a following operation supplies its own shift.

No dtype cast happens anywhere: whatever dtype `input` arrives in passes straight through matmul and addition unchanged.
