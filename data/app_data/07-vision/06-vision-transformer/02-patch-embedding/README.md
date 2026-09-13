---
name: vision-vit-patch-embedding
title: Patch Embedding
tags: [computer-vision, transformers, vision-transformer]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-patchify` turns an image into a sequence of flattened-patch vectors — but a transformer's tokens need to live in a fixed-size "embedding space" (dimension `d_model`) shared with everything else the transformer processes, and a flattened patch's raw pixel-vector length (`C * patch_size * patch_size`) has nothing to do with `d_model`. Something has to project every patch from "raw pixel space" into "embedding space." A word embedding table does this for word tokens by looking up a learned vector per word index; a ViT does the direct equivalent for patches with a learned linear projection, since a patch isn't a discrete symbol like a word — it's already a continuous vector.

### From theory to code

Theory says: apply a single, shared linear layer to every patch, mapping its raw `C*patch_size*patch_size`-dimensional pixel vector to a `d_model`-dimensional embedding — exactly the same linear transformation this curriculum's very first question already implemented for a completely different purpose.

Implement `patch_embedding(patches, weight, bias)` against that reasoning.

### Constraints

- `patches`: shape `(num_patches, C*patch_size*patch_size)`.
- `weight`: shape `(d_model, C*patch_size*patch_size)`.
- `bias`: shape `(d_model,)`.
- Returns shape `(num_patches, d_model)`.
- Every patch uses the exact same `weight` and `bias` (a single shared projection, not one per patch).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

This is not a new operation — it's `01-classical-ml/01-linear-regression/01-hypothesis-function`'s `linear(input, weight, bias)`, called with `patches` as the input.

</details>

<details>
<summary>Hint 2</summary>

`return linear(patches, weight, bias)` is the entire function body.

</details>

## Theory

### The simple version

Think of raw pixel values as a foreign language, and `d_model`-dimensional embedding space as the language every part of the transformer actually speaks. Patch embedding is the translator: it doesn't matter whether the "sentence" being translated is a word or a 16x16 pixel patch — the translation itself is the same kind of operation (a linear map) either way. This is exactly why a ViT can reuse a language transformer's entire architecture completely unmodified past this point: once patches have been embedded into `d_model`-dimensional vectors, the transformer genuinely cannot tell whether those vectors originally came from words or from image patches.

### The formula

```text
embeddings = patches @ weight.T + bias    # (num_patches, C*p*p) @ (C*p*p, d_model) -> (num_patches, d_model)
```

### How PyTorch actually implements this

Real ViT implementations (including the original paper's) almost never implement patchify and patch embedding as two separate steps — instead, they use a single `nn.Conv2d(in_channels=C, out_channels=d_model, kernel_size=patch_size, stride=patch_size)`. This works because a convolution with stride equal to its kernel size, applied to non-overlapping patches, computes exactly "flatten each patch, then apply the same linear layer to it" — the convolution's weight tensor, reshaped, IS the `(d_model, C*patch_size*patch_size)` linear weight this exercise uses directly. Keeping the two steps separate here (as `01-patchify` and this question) makes the underlying linear-algebra identity explicit rather than hiding it inside a convolution.

## Explanation

`linear(patches, weight, bias)` computes `patches @ weight.T + bias`: since `patches` is `(num_patches, C*p*p)` and `weight` is `(d_model, C*p*p)`, the matrix product `patches @ weight.T` has shape `(num_patches, d_model)` — every row of `patches` (one patch's flattened pixels) is projected by the same `weight` matrix into a `d_model`-dimensional embedding, and `bias` is added to every one of those projected rows identically. This is precisely "one shared linear layer applied to every patch independently": no patch gets its own weights, and the resulting `(num_patches, d_model)` sequence of embeddings is now in exactly the shape and space a transformer block (`05-transformers-llm/01-transformer-block`) expects its input sequence to be in.
