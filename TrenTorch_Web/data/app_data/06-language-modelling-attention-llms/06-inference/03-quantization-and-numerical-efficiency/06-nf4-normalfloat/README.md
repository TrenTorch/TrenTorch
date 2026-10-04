---
name: lm-nf4-normalfloat
title: NF4 Quantization
tags: [quantization, nf4, qlora]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Uniform 4-bit quantization spaces its 16 levels evenly, but trained weights are not spread evenly: they follow a bell curve, with most values near zero and few near the extremes. Evenly spaced levels waste resolution on the sparse tails and give too little to the crowded middle. **NF4** (NormalFloat 4) places its 16 levels at the _quantiles_ of a standard normal distribution, so each level is used about equally often. Weights are processed in blocks: each block is divided by its own absolute maximum so it lies in `[-1, 1]`, snapped to the nearest NF4 level, and stored as a 4-bit code plus one scale per block.

### From theory to code

Implement `nf4_quantize` and `nf4_dequantize`.

### Constraints

- Use the fixed 16-entry table `NF4_LEVELS` provided in the starter, sorted ascending from `-1.0` to `1.0` with an exact `0.0`.
- `nf4_quantize(w, block_size)`: `w` is a 1-D float array whose length is divisible by `block_size`. For each consecutive block compute `scale = max(|block|)`, normalize `block / scale` (use scale `1.0` for an all-zero block), and assign each value the index of the nearest NF4 level (lowest index on ties). Return `(codes, scales)` with `codes` an integer array of the same length as `w` and `scales` of length `len(w) / block_size`.
- `nf4_dequantize(codes, scales, block_size)` returns `NF4_LEVELS[codes] * scale_of_its_block`.

### Hints

<details>
<summary>Hint 1</summary>

`np.abs(x[:, None] - NF4_LEVELS[None, :]).argmin(axis=1)` finds the nearest level; `argmin` breaks ties toward the lowest index.

</details>

<details>
<summary>Hint 2</summary>

Reshape to `(num_blocks, block_size)` so the per-block maximum is one reduction.

</details>

## Theory

### The simple version

Imagine fitting a ruler to measure people. Marks every centimetre waste effort at heights nobody has. Marking more finely where most people stand, and sparsely at the extremes, gives a better measurement for the same number of marks.

### The formula

$$
s_b = \max_{i\in b}|w_i|, \qquad q_i = \arg\min_j \big|\tfrac{w_i}{s_b} - \ell_j\big|, \qquad \hat w_i = \ell_{q_i}\, s_b
$$

where $\ell_j$ are the NF4 levels, roughly the quantiles of $\mathcal{N}(0,1)$ rescaled to $[-1, 1]$. For normally distributed weights the expected error is lower than for evenly spaced 4-bit levels.

### How this is done in practice

QLoRA introduced NF4 and `bitsandbytes` implements it with block size 64 and optional _double quantization_ of the scales. Weights are dequantized on the fly inside the matrix multiplication, so memory drops about 4x while the arithmetic stays in 16-bit.

## Explanation

The function normalizes each block, snaps to the nearest table entry and keeps the scale. The test comparing NF4 with evenly spaced levels on normally distributed data is the empirical reason the format exists.
