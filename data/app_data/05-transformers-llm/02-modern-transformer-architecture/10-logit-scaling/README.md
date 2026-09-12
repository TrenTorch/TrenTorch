---
name: txf-modern-logit-scaling
title: 'Logit scaling before the final softmax'
tags: [transformers]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[04-seq-modeling/04-attention/01-scaled-dot-product-attention]` divided raw attention scores by `1/sqrt(d_k)` for a concrete numerical reason: a dot product between two `d_k`-dimensional vectors has variance proportional to `d_k`, so without scaling, larger dimensions produce larger-magnitude scores, pushing `softmax` toward its SATURATED regime (extremely close to one-hot, near-zero gradient almost everywhere). `[09-untied-embeddings]`'s final output projection, `hidden_states @ output_weight.T`, is ALSO a dot product, between a `d_model`-dimensional hidden state and each vocabulary word's `d_model`-dimensional row, and it has the EXACT SAME statistical problem: the resulting logits' magnitude naturally grows with `d_model`, and without any correction, a model with a larger hidden dimension produces disproportionately SHARPER, more overconfident next-token probability distributions, purely as a side effect of its width, unrelated to how genuinely confident the underlying prediction actually should be.

Dividing the final logits by `1/sqrt(d_model)` before softmax is the exact same fix, applied at the exact same conceptual spot in the computation, just one layer later in the model, at the very END rather than inside every attention call.

### From theory to code

Implement `scale_logits_before_softmax(logits, d_model)`, a direct `logits / sqrt(d_model)`.

### Constraints

- Scales by `1 / sqrt(d_model)`, not `1 / d_model` (an easy, meaningfully different mistake, `[01-scaled-dot-product-attention]`'s own scaling used the same square root for the same reason).
- Applied to the LOGITS (the RAW output of `[09-untied-embeddings]`'s output projection), strictly BEFORE softmax is computed, never after.
- A purely elementwise, linear operation: scaling every logit by the same constant factor.

### Hints

<details>
<summary>Hint 1: The entire implementation</summary>

`return logits / np.sqrt(d_model)`. The genuine content of this question is recognizing WHERE and WHY this exact correction is needed, not any computational complexity in applying it.

</details>

## Theory

### The simple version

`[01-scaled-dot-product-attention]`'s Theory section already told this story once: a panel of judges (dimensions) each casting a small, roughly independent vote toward a score, and the MORE judges on the panel, the more extreme the combined, UNNORMALIZED total tends to get, purely from having more judges, regardless of how strongly any individual judge actually felt. Dividing by the square root of the panel size corrects for exactly this effect, restoring a score whose typical MAGNITUDE stays roughly comparable no matter how many judges (dimensions) are actually voting. The vocabulary logits at the very end of a language model face the identical situation, just with `d_model`-many "judges" instead of `d_k`-many.

### The formula

```
scaled_logits = logits / sqrt(d_model)
probabilities = softmax(scaled_logits)
```

Directly parallel to `[01-scaled-dot-product-attention]`'s `scores / sqrt(d_k)`, just applied to the model's FINAL vocabulary-sized output instead of an intermediate attention score matrix.

### How PyTorch actually implements this

Not every model architecture applies this scaling (many rely on careful weight initialization and layer normalization instead to keep logit magnitudes reasonable without it), but architectures using "muP" (Maximal Update Parametrization, Yang et al. 2022) and similar width-invariant parametrizations apply exactly this kind of output-scaling correction specifically so that a model's TRAINING dynamics (learning rate, initialization scale) transfer cleanly across different values of `d_model`, without needing to be re-tuned from scratch every time the model's width changes; some implementations fold an equivalent factor directly into the output projection's weight initialization instead of applying it as a separate scaling step at inference. `[01-scaled-dot-product-attention]`'s original motivation (keep softmax's input in a well-conditioned range, regardless of dimensionality) reappears here in essentially its purest form, applied to a language model's single most consequential softmax: the one that actually decides what word comes next.

## Explanation

`scale_logits_before_softmax` divides every logit by `sqrt(d_model)`, directly countering the fact that `[09-untied-embeddings]`'s output projection is a `d_model`-dimensional dot product whose typical magnitude grows with `sqrt(d_model)` for randomly-scaled weights, exactly the same statistical phenomenon `[01-scaled-dot-product-attention]`'s `1/sqrt(d_k)` scaling was designed to counteract for attention scores. Left unscaled, a model with a large hidden dimension would produce logits large enough to push its final `softmax` into an artificially over-sharpened, near one-hot regime, not because the underlying prediction is genuinely more confident, but purely as a side effect of the model's width. Scaling by the same square-root factor keeps the logits' typical magnitude, and therefore the sharpness of the resulting next-token probability distribution, in a comparable, well-behaved range regardless of `d_model`.
