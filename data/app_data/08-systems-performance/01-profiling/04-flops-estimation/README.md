---
name: systems-perf-flops-estimation
title: FLOPs Estimation (Linear/Conv)
tags: [mlops, profiling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-parameter-counting` counts how many numbers a model has, and `03-memory-footprint-estimation` counts how many bytes storing them costs — neither says anything about how much _compute_ a forward pass actually takes. Two models can have the same parameter count and wildly different runtime cost (a `Linear` layer applied once vs. a `Conv2d` layer's kernel sliding across every spatial position), so a separate estimate is needed: FLOPs, the number of individual floating-point multiply/add operations a forward pass performs.

### From theory to code

Implement `linear_flops(batch_size, in_features, out_features, bias=True)` and `conv2d_flops(batch_size, in_channels, out_channels, kernel_size, output_height, output_width, bias=True)`, each returning the total FLOP count for one forward pass of that layer type.

### Constraints

- Every multiply-accumulate (one multiply, one add) counts as `2` FLOPs — the standard convention used by real profiling tools.
- `linear_flops`: `2 * batch_size * in_features * out_features` multiply-add FLOPs, plus `batch_size * out_features` more if `bias=True` (one addition per output element).
- `conv2d_flops`: assumes a square kernel, no groups, no dilation. Each of `batch_size * out_channels * output_height * output_width` output positions costs `in_channels * kernel_size * kernel_size` multiply-adds; add one more FLOP per output position if `bias=True`.
- `bias` defaults to `True` in both functions.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute the total number of output _elements_ first (`batch_size * out_features` for Linear, `batch_size * out_channels * output_height * output_width` for Conv2d) — everything else is "how much work does producing ONE output element cost," multiplied by that count.

</details>

<details>
<summary>Hint 2</summary>

One output element of a Conv2d is a dot product over the kernel's entire receptive field: `in_channels * kernel_size * kernel_size` multiply-adds, exactly analogous to Linear's `in_features` multiply-adds per output element.

</details>

## Theory

### The simple version

Every single output number a layer produces is the result of some fixed amount of arithmetic — for a Linear layer, one output is a dot product between the input and one row of the weight matrix; for a Conv2d layer, one output is a dot product between the kernel and the patch of input it's currently looking at. Multiply "how much arithmetic makes one output number" by "how many output numbers there are," and that's the layer's total compute cost for one forward pass.

### The formula

```text
linear_flops:
    multiply_adds = batch_size * in_features * out_features
    flops = 2 * multiply_adds + (batch_size * out_features if bias else 0)

conv2d_flops:
    output_positions = batch_size * out_channels * output_height * output_width
    multiply_adds_per_position = in_channels * kernel_size * kernel_size
    flops = 2 * output_positions * multiply_adds_per_position + (output_positions if bias else 0)
```

### How PyTorch actually implements this

Context only, untested by your submission: PyTorch itself doesn't report FLOP counts — dedicated profiling tools like Meta's `fvcore` (`FlopCountAnalysis`) and the third-party `thop` library hook into a model's forward pass and apply exactly this per-layer-type formula (2 FLOPs per multiply-accumulate) to produce the FLOP counts widely reported in papers comparing model efficiency. This exercise's formulas match that same standard, tool-independent convention rather than any one specific library's internal computation.

## Explanation

`linear_flops` computes `multiply_adds = batch_size * in_features * out_features` (one multiply-add per input feature, per output feature, per batch element), doubles it for the standard 2-FLOPs-per-multiply-add convention, and adds `batch_size * out_features` more when `bias=True` (one addition per output element, applied after the matrix multiply).

`conv2d_flops` computes `output_positions`, the total count of individual output values across every batch element, output channel, and spatial position, then multiplies by `multiply_adds_per_position = in_channels * kernel_size * kernel_size` (the size of the dot product each output value requires), doubles for the FLOPs convention, and adds one more FLOP per output position when `bias=True`.
