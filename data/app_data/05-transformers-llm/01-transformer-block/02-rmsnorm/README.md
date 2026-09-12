---
name: txf-block-rmsnorm
title: 'Stretch: RMSNorm (alternative to LayerNorm)'
tags: [transformers]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[01-layer-normalization-forward]`'s LayerNorm does two separate things: it CENTERS a position's feature vector (subtracts the mean) and it RESCALES it (divides by the standard deviation), before applying a learned `gamma`/`beta`. Zhang & Sennrich (2019) asked a pointed empirical question: how much of LayerNorm's benefit actually comes from the re-scaling, versus the re-centering? Their finding, since adopted by LLaMA, PaLM, Mistral, and most other modern large language models, was that the RESCALING is doing almost all of the useful work, and the mean-centering step can simply be dropped, with training stability and final model quality both essentially unaffected.

The result, RMSNorm, is a strictly SIMPLER, cheaper normalization: no mean to compute, no `beta` shift to learn, just a single division by the vector's own root-mean-square. Fewer operations per call, fewer parameters to learn, and (because it computes only ONE statistic instead of two) a meaningfully cheaper operation to run billions of times over during training and inference, a real, measurable cost saving at the scale modern LLMs run at.

### From theory to code

Implement `rmsnorm_forward(x, gamma, eps)`. Compute the root-mean-square of `x` along its LAST axis (`sqrt(mean(x^2) + eps)`), divide `x` by that value, then apply the learned per-feature multiplicative scale `gamma` (there is no `beta`, unlike `[01-layer-normalization-forward]`).

### Constraints

- No mean-subtraction anywhere: RMSNorm normalizes using only the SECOND moment (`mean(x^2)`), never the first (`mean(x)`).
- `eps` is added INSIDE the square root, exactly like `[01-layer-normalization-forward]`, to avoid dividing by zero.
- There is no `beta` parameter: the only learned parameter is the multiplicative `gamma`.
- Statistics are computed along the LAST axis, independently per position, exactly like `[01-layer-normalization-forward]`.

### Hints

<details>
<summary>Hint 1: The root-mean-square</summary>

`rms = np.sqrt(np.mean(x**2, axis=-1, keepdims=True) + eps)`. This is the ONLY statistic RMSNorm needs, no separate mean computation at all.

</details>

<details>
<summary>Hint 2: Normalizing and scaling</summary>

`return gamma * (x / rms)`. Compare directly against `[01-layer-normalization-forward]`'s `gamma * ((x - mean) / sqrt(var + eps)) + beta`: RMSNorm is that formula with the `- mean` term and the `+ beta` term both removed.

</details>

## Theory

### The simple version

`[01-layer-normalization-forward]`'s classroom-transcript analogy standardized each student's grades to a common scale AND recentered them around zero. RMSNorm keeps only the rescaling: it asks "how large are this student's grades, TYPICALLY" (their root-mean-square, a measure of overall magnitude that doesn't care whether the grades run high or low, only how spread out they are from zero) and divides every grade by that one number, without first shifting everything to be centered on the class average.

### The formula

```
rms = sqrt(mean(x^2, axis=-1) + eps)
output = gamma * (x / rms)
```

Contrast directly with `[01-layer-normalization-forward]`: `output = gamma * ((x - mean) / sqrt(var + eps)) + beta`. RMSNorm is exactly that formula with `mean` (the centering term) and `beta` (the additive shift) both dropped, leaving only the rescaling by a second-moment statistic.

### How PyTorch actually implements this

`torch.nn.RMSNorm(normalized_shape, eps)` implements precisely this formula (this question's implementation matches its output exactly, verified directly): `weight` is `gamma`, the sole learned parameter, initialized to `1`. Because RMSNorm skips computing a mean, it requires meaningfully fewer floating-point operations per call than LayerNorm, and modern LLM training/inference code takes advantage of this directly: fused CUDA kernels for RMSNorm are a standard optimization target in serving frameworks precisely because the operation runs so many times per forward pass. `[05-swiglu-ffn]`, later in this same track, pairs naturally with RMSNorm (both are the LLaMA-style choice over LayerNorm/plain-ReLU-FFN), since real modern architectures tend to adopt both changes together rather than one in isolation.

## Explanation

`rmsnorm_forward` computes `rms = sqrt(mean(x**2, axis=-1, keepdims=True) + eps)`, the root-mean-square of each position's feature vector, the SOLE statistic RMSNorm needs (no separate mean of `x` itself is ever computed). Dividing `x` by `rms` rescales every position to have a root-mean-square of (approximately) `1`, without recentering it around zero first. The final `gamma * (x / rms)` applies the learned per-feature multiplicative scale, the only learned parameter RMSNorm has, restoring whatever magnitude the network actually needs at that feature, without `[01-layer-normalization-forward]`'s separate additive `beta` term.
