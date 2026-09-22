---
name: potd-sensor-fusion-linear-layer
title: 'SENSOR FUSION LAYER'
tags: [neural-networks]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Neural Networks

---

### Story

A single linear layer fuses concatenated radar and camera features before Tesla's perception stack
does anything more sophisticated: the "hello world" layer of the whole pipeline, but it has to be
bit-exact.

---

### The Math

```
y = W x + b
```

### Input Format

```
d_in d_out
W (d_out x d_in, row-major)
b (d_out values)
x (d_in values)
```

### Output Format

`y`, `d_out` values, 6 decimals.

### Constraints

- `1 <= d_in, d_out <= 256`
- Time limit: 1.0 second.

---

### Example

**Input**

```
3 2
1 0 1
0 1 1
0.5 -0.5
1 2 3
```

**Output**

```
4.500000 4.500000
```

## Theory

### The simple version

A linear layer combines several input numbers into one or more output numbers by weighting each input and adding a baseline. It is the same idea as a weighted average, just with a bias term added on top.

### The shape convention is fixed

`W` is given already shaped `(d_out, d_in)`, so the multiply is literally `W @ x`, no transpose. A
transpose bug is invisible when `d_in == d_out`, since a wrongly-transposed square matrix still
produces an output of the right shape, just the wrong numbers. Testing with `d_in != d_out` turns
that silent bug into a dimension mismatch.

### No activation

This is a raw linear layer: no ReLU, no sigmoid, nothing clamping the output. If `b` is large and
negative, the result is simply negative; there is nothing to clamp.

### `d_out = 1`

With a single output unit, the result is one number rather than a length-1 vector conceptually, but
the function still returns a length-1 array; only the formatting of a single value differs.

## Explanation

`linear_forward` computes `W @ x + b` in one NumPy expression: `W @ x` is the matrix-vector product
(efficient at up to `256 x 256`, not a nested Python loop), and adding `b` broadcasts elementwise
over the result. Because `W` is passed in already shaped `(d_out, d_in)`, no transpose or reshape is
needed before the multiply, which is exactly the shape convention the problem statement fixes to
rule out a transpose ambiguity.
