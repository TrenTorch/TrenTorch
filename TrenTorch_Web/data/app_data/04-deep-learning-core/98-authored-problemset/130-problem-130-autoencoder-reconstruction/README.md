---
name: problem-130-autoencoder-reconstruction
title: Autoencoder Reconstruction
tags: [dl-core, case-study, hard, autoencoders., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(x, recon)`. Compute reconstruction loss for an encoder-decoder output. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Flipkart is scenario context only; this is not an official Flipkart interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 3], [1, 3, 2])
```

**Output**

```text
0.6666666666666666
```

**Explanation.** Compute reconstruction loss for an encoder-decoder output.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
0.6666666666666666
```

### Hint

mean squared reconstruction error

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Autoencoder Reconstruction?

Compute reconstruction loss for an encoder-decoder output. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Autoencoder Reconstruction supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **mean squared reconstruction error**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(np.mean((np.asarray(x) - np.asarray(recon)) ** 2))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3],[1,3,2])` returns `0.6666666666666666`. Reversing its observation rows returns `0.6666666666666666`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.mean`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(np.mean((np.asarray(x) - np.asarray(recon)) ** 2))` after preparing the intermediates for Autoencoder Reconstruction. `np.asarray`, `np.mean` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
