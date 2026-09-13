---
name: dl-core-elementwise-ops
title: Elementwise ops
tags: [deep-learning, tensors]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-hypothesis-function`'s `input @ weight.T` combined many elements together into each output value, that's what matrix multiplication does. Most of the arithmetic inside a neural network isn't like that at all: adding a bias, subtracting a target from a prediction, scaling a gradient, these all act on corresponding positions independently, one input element in, one output element out, no mixing across positions. That's "elementwise," and it's the most common shape of computation in this whole curriculum, worth its own question before anything more complex is layered on top.

### From theory to code

Implement `add`, `sub`, `mul`, `div`, `power`, each mirroring the `torch.*` function (and the operator, `+`/`-`/`*`/`/`/`**`) of the same name. Four of the five are direct one-line translations; `div` is the one place Theory's warning about integer-vs-float division actually has to be handled deliberately rather than left to whichever operator happens to get used.

### Constraints

- All five functions operate elementwise, broadcasting `a` and `b` the normal NumPy way (including a scalar against an array).
- `div(a, b)` always returns a floating-point result, even when both `a` and `b` are integer arrays — never Python's `//` floor-division behavior.
- No explicit loops over array elements; each function is a single vectorized expression.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Four of these five functions are exactly the Python operator you'd expect (`+`, `-`, `*`, `**`) applied directly to `a` and `b`. Only one of them needs something other than its bare operator.

</details>

<details>
<summary>Hint 2</summary>

A plain `a / b` between two integer NumPy arrays already returns a float in NumPy (NumPy's `/` is true division by default, unlike Python's `//`). The point of `div` isn't to fix a bug NumPy has, it's to name the function NumPy's own `/` operator actually calls internally, so the choice reads as deliberate: `np.true_divide`.

</details>

## Theory

### The simple version

Picture two equally-long rows of numbers stacked on top of each other. An elementwise operation walks down the stack one column at a time, combining only the two numbers directly above and below each other, it never reaches sideways to a different column. Whatever shape the rows have, the result has the same shape, one output per input pair.

### The formula

```text
add(a, b)_i   = a_i + b_i
sub(a, b)_i   = a_i - b_i
mul(a, b)_i   = a_i * b_i
div(a, b)_i   = a_i / b_i     (true division, always float, even for integer inputs)
power(a, b)_i = a_i ** b_i
```

### How PyTorch actually implements this

`torch.add`/`torch.sub`/`torch.mul`/`torch.div`/`torch.pow` (and the operators that call them) are the real PyTorch equivalents of these five functions. `torch.div` specifically documents true division as its default behavior, dividing two integer tensors still returns a floating-point tensor, not a truncated integer one; this repo's `tests.py` doesn't bake in a PyTorch-generated numeric oracle for this question, so this is a description of the real API's documented behavior, not a claim about specific numbers beyond what `np.true_divide` itself verifiably produces.

## Explanation

`add`, `sub`, `mul`, `power` in `solution.py` are direct one-line calls to the corresponding NumPy operator (`a + b`, `a - b`, `a * b`, `a**b`), NumPy's own broadcasting and dtype-promotion rules already match what `torch`'s equivalents do for these operations, there's nothing to add on top.

`div` calls `np.true_divide(a, b)` explicitly rather than a bare `a / b`. This guarantees floating-point division regardless of whether `a`/`b` are integer or float arrays, `np.true_divide` is the exact function NumPy's own `/` operator calls internally, so naming it explicitly here is about being unambiguous that this is a deliberate choice matching `torch.div`'s behavior, not an accident of which operator happened to be used. `test_div_of_two_integer_arrays_returns_true_division_not_floor_division` and `test_div_result_dtype_is_floating_even_for_integer_inputs` both target exactly this: `div(np.array([7]), np.array([2]))` must be `3.5`, not `3`.
