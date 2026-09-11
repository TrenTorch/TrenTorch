---
name: linear-regression-mse-loss
title: Mean Squared Error Loss
tags: [classical-ml, linear-regression, loss-functions]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A model that guesses is only useful if you can measure how wrong its guesses are. One number, one clear rule: given what the model predicted and what actually happened, produce a single score where lower means better.

The obvious first idea, average the raw difference, breaks immediately: a guess that's 5 too high and one that's 5 too low average out to zero error, which is wrong, both guesses were equally bad. Squaring each difference before averaging fixes that (every error becomes positive) and, as a side effect, punishes big misses harder than small ones: an error of 10 contributes 100, not 10. That score is mean squared error, and it's what `torch.nn.functional.mse_loss` computes.

### From theory to code

Theory derives the elementwise error, square each difference, then a reduction step: average them (`'mean'`), add them up (`'sum'`), or hand back every squared error untouched (`'none'`). Real PyTorch exposes all three, because different callers want different things: training almost always wants `'mean'` (a batch-size-independent score), some manual bookkeeping wants `'sum'`, and anything that needs to look at individual errors before combining them, like weighting some samples more than others, needs `'none'`.

Implement `mse_loss(input, target, reduction='mean')` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `input`, `target`: same shape as each other, any shape.
- `reduction`: `'mean'`, `'sum'`, or `'none'`. Anything else raises `ValueError`.
- Return type depends on `reduction`: a plain Python `float` for `'mean'`/`'sum'`, an array shaped like `input` for `'none'`.
- One vectorized expression per branch, no loop over elements.
- `input` and `target` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute the elementwise squared error once, before branching on `reduction`. All three modes start from the exact same array.

</details>

<details>
<summary>Hint 2</summary>

`'mean'` and `'sum'` both need a `float(...)` cast around a NumPy reduction. Returning a bare NumPy scalar (like `np.float64`) instead of a real `float` is a common, easy-to-miss mismatch.

</details>

<details>
<summary>Hint 3</summary>

Handle the invalid-reduction case last, as an `else` that raises `ValueError`, not a silent fallback to one of the other two. A typo in the caller's `reduction` argument should never quietly compute the wrong thing.

</details>

## Theory

### The simple version

Imagine a teacher grading guesses against the real answer. Missing by 1 costs 1 point. Missing by 10 costs 100 points, not 10, because a big miss is worse than ten small ones combined. Add up every student's points and divide by the class size, and you get one number: how bad the guessing was, on average, for one guess.

### The formula

For predictions `ŷ₁, ..., ŷₙ` against targets `y₁, ..., yₙ`:

```text
MSE = (1/n) * [ (ŷ₁ - y₁)² + (ŷ₂ - y₂)² + ... + (ŷₙ - yₙ)² ]
```

### Why squared, not absolute value

Squaring isn't the only way to make every error positive. `abs(ŷ - y)` would work too, and is a real, named loss (L1 loss). Squared error wins for training specifically because it's smooth: its derivative at any point is proportional to the error itself, `2(ŷ - y)`, which vanishes gracefully to zero right where the prediction is correct. Absolute error's derivative is a constant `+1` or `-1` everywhere except exactly at zero, where it's undefined, so gradient descent never actually slows down as it approaches a perfect fit; it can overshoot and oscillate instead of settling. Squared error also matches a specific statistical assumption (that prediction errors are Gaussian noise), which is why it's the default choice for regression rather than an arbitrary one.

### The reduction gotcha that breaks real code

Q1's Theory ended on a warning: a `(batch_size, 1)` prediction minus a `(batch_size,)` target silently broadcasts to `(batch_size, batch_size)` instead of erroring. This is exactly where that bites. Feed a squeezed and an unsqueezed array into a loss function and both run without complaint, computing something that looks like a real number and is completely wrong. The fix isn't in this function, it's in never producing the wrong shape in the first place, which is why 01-hypothesis-function's `linear` refuses to squeeze its output.

### How PyTorch actually implements this

`torch.nn.functional.mse_loss` has evolved as an API. Its real signature is `mse_loss(input, target, size_average=None, reduce=None, reduction='mean')`. `size_average` and `reduce` are two older booleans from an earlier version of PyTorch (before a single `reduction` string existed), kept only so old code doesn't break. They're deprecated: don't use them in new code, and PyTorch's own docs say so directly.

`torch.nn.MSELoss` is the module wrapper, same relationship `nn.Linear` has to `F.linear`: it stores `reduction` as a constructor argument, and `forward(input, target)` just calls into the functional version. Like `F.linear`, the real implementation is a fused ATen kernel, not literally `(input - target) ** 2` followed by a separate reduction call, so autograd has one gradient formula for the whole operation instead of one for subtraction, one for squaring, and one for the reduction, chained together.

One more real detail: PyTorch's `mse_loss` allows `input` and `target` shapes that are broadcastable but not identical, and if they're not exactly equal it prints a `UserWarning` naming the two shapes rather than silently proceeding. That warning exists because of the exact bug this question's Theory just described, it's PyTorch's own defense against it, added after enough people hit it in production.

## Explanation

`(input - target) ** 2` computes the elementwise squared error once, reused by all three branches. `np.mean` and `np.sum` both operate over every element regardless of the input's shape (a `(batch_size, out_features)` array reduces fully, not per row), matching what `reduction='mean'`/`'sum'` mean in real PyTorch.

`float(...)` wraps both scalar reductions because `np.mean`/`np.sum` return a NumPy scalar type (`np.float64`), not a plain Python `float`, and the constraint is a real `float`. `reduction='none'` returns the squared-error array itself, no cast, since the constraint there is an array shaped like `input`.

The `else: raise ValueError(...)` branch exists because a typo'd `reduction` argument should fail loudly at the call site, not silently compute a wrong number that only shows up as a confusing downstream result.
