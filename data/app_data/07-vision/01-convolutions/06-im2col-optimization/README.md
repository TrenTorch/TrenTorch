---
name: vision-conv-im2col
title: 'Stretch: im2col — Turning Convolution into One Matrix Multiply'
tags: [computer-vision, convolutions, optimization]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`05-multiple-output-filters` computes one number per `(filter, output position)` pair via a Python loop, each iteration doing its own small elementwise-multiply-and-sum. That's correct, but it's exactly the kind of code that's slow in Python and doesn't map well onto how real hardware (GPUs, and CPUs with BLAS libraries) actually gets its speed: from doing a small number of very large matrix multiplies, not a huge number of tiny reductions.

im2col is the trick that closes that gap: gather every sliding-window patch the convolution would visit into the rows of one big matrix, flatten every filter into the rows of another, and replace the entire nested loop with a single matrix multiply. Same answer, computed the way real convolution implementations actually compute it.

### From theory to code

Theory says: every output position corresponds to one row of a "columns" matrix (the flattened patch at that position), and every output filter corresponds to one row of a flattened kernel matrix. Multiplying those two matrices together produces every `(position, filter)` output value at once.

Implement `conv2d_im2col(image, kernel)` against that reasoning — same contract as `05-multiple-output-filters`, different computation strategy.

### Constraints

- `image`: shape `(C_in, H, W)`. `kernel`: shape `(C_out, C_in, kH, kW)`.
- Output: shape `(C_out, H - kH + 1, W - kW + 1)`, numerically identical to `05-multiple-output-filters`'s output for the same inputs.
- The reduction over `(C_in, kH, kW)` for every `(position, filter)` pair must happen via a single matrix multiply, not a Python loop over output positions.
- `image` and `kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.lib.stride_tricks.sliding_window_view(image, (kH, kW), axis=(1, 2))` returns every `(kH, kW)` patch, for every channel and every valid position, without a Python loop — shape `(C_in, out_h, out_w, kH, kW)`.

</details>

<details>
<summary>Hint 2</summary>

Rearrange those patches so each output position becomes one row: transpose to put `out_h, out_w` first, then reshape to `(out_h*out_w, C_in*kH*kW)`. Flatten `kernel` to `(C_out, C_in*kH*kW)` the same way, then it's one matrix multiply: `cols @ kernel_flat.T`, shape `(out_h*out_w, C_out)`.

</details>

<details>
<summary>Hint 3</summary>

The matmul's output has positions along one axis and filters along the other — transpose and reshape it back to `(C_out, out_h, out_w)` to match the expected output shape.

</details>

## Theory

### The simple version

Instead of visiting every window position one at a time and doing a tiny sum each time, first lay out every window, side by side, as rows of one big table. Lay out every filter as rows of a second table. One matrix multiply between the two tables computes every window-filter combination's answer simultaneously — the same total work, but done as one large, hardware-friendly operation instead of many small Python-level ones.

### The formula

```text
cols          = every (C_in, kH, kW) patch, flattened to a row -> shape (out_h*out_w, C_in*kH*kW)
kernel_flat   = every filter, flattened to a row               -> shape (C_out, C_in*kH*kW)
out_flat      = cols @ kernel_flat.T                            -> shape (out_h*out_w, C_out)
output        = out_flat.T.reshape(C_out, out_h, out_w)
```

Each row of `cols` dotted with each row of `kernel_flat` reproduces exactly the elementwise-multiply-and-sum `05-multiple-output-filters` computes per `(position, filter)` pair — matrix multiplication IS a batch of dot products, which is precisely what this computation already was.

### How PyTorch actually implements this

Real convolution implementations (cuDNN on GPU, and CPU BLAS-backed implementations) use this exact im2col-then-GEMM strategy, or closely related direct-convolution kernels tuned to avoid materializing the full `cols` matrix (which can be large) while still doing the reduction as dense matrix multiplies under the hood. `torch.nn.functional.conv2d` computes the identical numerical result as this question — the difference is purely how the reduction is scheduled on hardware, never what number comes out.

## Explanation

`sliding_window_view` produces every patch as a view into the original `image` array with no copying — reshaping and transposing it into `cols` is what actually materializes the patches as a real matrix (the one meaningful cost of im2col: patches overlap, so `cols` is a bigger allocation than `image` itself). `kernel.reshape(C_out, C_in*kH*kW)` flattens each filter's `(C_in, kH, kW)` weights into one row, in the same channel/row/column order the patches were flattened in — the two flattenings have to agree, element for element, for the matrix multiply's dot products to compute the right sum. `cols @ kernel_flat.T` then computes every `(position, filter)` pair's dot product in one call, and the final transpose-and-reshape puts the result back into the `(C_out, out_h, out_w)` shape the direct-loop version in `05-multiple-output-filters` already produces — same answer, reached by one big matrix multiply instead of many small ones.
