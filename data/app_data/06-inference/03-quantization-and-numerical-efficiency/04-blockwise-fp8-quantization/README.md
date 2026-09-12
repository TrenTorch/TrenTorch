---
name: inf-quant-fp8-blockwise
title: 'Block-Wise FP8 (E4M3-style) Quantization'
tags: [inference, quantization, fp8, block-wise]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[03-groupwise-int4-quantization]`'s INT4 uses a fixed absolute step size within each group, so small values within a group still lose relative precision compared to the group's largest value. FP8 (E4M3: 1 sign bit, 4 exponent bits, 3 mantissa bits) keeps a floating-point-style exponent instead, so its relative precision stays roughly constant across magnitudes. Implement a simplified block-wise FP8 quantization scheme: split a weight matrix into fixed-size 2D blocks, compute one scale per block, and quantize each block's values into a simulated 8-bit floating-point format with 4 exponent bits and 3 mantissa bits.

### From theory to code

```
scale[block] = max(|W[block]|) / 448          -- FP8 E4M3 max representable magnitude
x_scaled = W[block] / scale[block]
x_fp8 = round_to_3_mantissa_bits(x_scaled)     -- simulated via frexp/ldexp
x_hat = x_fp8 * scale[block]
```

### Constraints

- Rows and columns must each be evenly divisible by `block_rows`/`block_cols` respectively.
- One independent scale per 2D block, from that block's max absolute value divided by 448 (E4M3's max magnitude).
- Simulate 3-mantissa-bit rounding on the scaled values using frexp/ldexp (round mantissa to nearest 1/8 step).
- Return the simulated-FP8 quantized values (still floats, since FP8 isn't a native NumPy dtype), the per-block scale matrix, and the dequantized reconstruction.

### Hints

<details>
<summary>Hint: Simulating FP8 rounding</summary>

`np.frexp` splits a float into a mantissa in `[0.5, 1)` and an integer exponent — round the mantissa to `2**-3` granularity, then reconstruct with `np.ldexp`. Compute one scale per 2D tile using nested reshaping similar to group-wise quantization, but over 2 axes instead of 1.

</details>

## Theory

### The simple version

INT quantization is like a ruler with evenly-spaced tick marks — great near the largest value, coarse near small ones. FP8 is like a ruler whose tick marks get closer together near zero and farther apart near the extremes, so a value's RELATIVE precision (how many significant digits it keeps) stays roughly constant no matter its magnitude — a tiny value keeps about as many meaningful digits as a huge one.

### The formula

```
scale[block] = max(|W[block]|) / 448
x_fp8 = round_to_3_mantissa_bits(W[block] / scale[block])
x_hat = x_fp8 * scale[block]
```

Block-wise FP8 (as used for DeepSeek-V3-style FP8 training/inference) scales each small 2D block of the weight matrix independently, so a single large outlier only distorts its own local block instead of coarsening the ENTIRE matrix's precision the way one global scale would.

### How PyTorch actually implements this

PyTorch has no public `frexp`/`ldexp`-based mantissa rounding helper built for arbitrary bit-widths; the NumPy routine here is typically run once offline to produce simulated FP8 weights, or replaced with `torch.float8_e4m3fn` casts directly where hardware/library support exists.

## Explanation

`np.frexp` decomposes any nonzero float into `mantissa * 2**exponent` with the mantissa confined to `[0.5, 1)`; rounding that mantissa to the nearest multiple of `2**-bits` and reconstructing with `np.ldexp` is precisely what a 3-mantissa-bit floating-point format does — the RELATIVE rounding error stays roughly constant regardless of the exponent, unlike INT quantization's constant ABSOLUTE step size. This is the fundamental difference from `[01-symmetric-int8-quantization]` and `[03-groupwise-int4-quantization]`: those formats have a fixed number of representable VALUES spread linearly across a range, while FP8 has a fixed number of representable SIGNIFICANT DIGITS, spread logarithmically — which is exactly why small values inside a block (e.g. `0.01` next to a block max of `100`) are NOT crushed to zero the way they would be under INT8's linear spacing.
