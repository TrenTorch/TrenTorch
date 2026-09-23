---
name: vision-vit-patchify
title: Patchify an Image into Fixed-Size Patches
tags: [computer-vision, transformers, vision-transformer]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A transformer operates on a _sequence_ of tokens — that's the entire premise of everything in `05-transformers-llm`'s attention and transformer-block questions. An image isn't naturally a sequence at all; it's a 2D (or 3D, with channels) grid. The Vision Transformer's founding idea is disarmingly simple: chop the image into a grid of fixed-size square patches, treat each patch as if it were one "token," and feed the resulting sequence of patches through an ordinary transformer, completely unmodified from how it processes word tokens.

### From theory to code

Theory says: split the image into a regular grid of non-overlapping `patch_size x patch_size` squares (covering every channel), then flatten each individual patch (all its channels and pixels) down into one single vector — turning a `(C, H, W)` image into a `(num_patches, C*patch_size*patch_size)` sequence of flattened-patch vectors.

Implement `patchify(image, patch_size)` against that reasoning.

### Constraints

- `image`: shape `(C, H, W)`, with both `H` and `W` divisible by `patch_size`.
- `patch_size`: side length of each square patch.
- Returns shape `(num_patches, C * patch_size * patch_size)`, where `num_patches = (H // patch_size) * (W // patch_size)`.
- Patches are ordered row-major over the patch grid: left-to-right within a row of patches, then top-to-bottom across rows.
- `image` is never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`image.reshape(C, n_h, patch_size, n_w, patch_size)` (with `n_h = H // patch_size`, `n_w = W // patch_size`) splits `H` and `W` into "which patch" and "which pixel within that patch" without moving any data — reshape alone can do this because `H` and `W` are exact multiples of `patch_size`.

</details>

<details>
<summary>Hint 2</summary>

After that reshape, `.transpose(1, 3, 0, 2, 4)` moves the two grid axes (`n_h`, `n_w`) to the front, giving shape `(n_h, n_w, C, patch_size, patch_size)` — now a final `.reshape(n_h * n_w, C * patch_size * patch_size)` flattens the patch grid into a sequence and each patch's own data into one vector, in one step.

</details>

## Theory

### The simple version

Imagine cutting a photograph into a grid of small square tiles, like a jigsaw puzzle laid out in its box — then instead of keeping the 2D grid arrangement, you line the tiles up in a single row, left-to-right, top-row-first. Each tile, flattened out, becomes one "word" in a sentence the transformer can read — a ViT doesn't know or care that its input used to be a 2D image at all; as far as the transformer is concerned, it's just processing a sequence of vectors, exactly like it would process a sequence of word embeddings.

### The formula

```text
n_h, n_w = H // patch_size, W // patch_size
patches  = image.reshape(C, n_h, patch_size, n_w, patch_size)
patches  = patches.transpose(1, 3, 0, 2, 4)          # (n_h, n_w, C, patch_size, patch_size)
return patches.reshape(n_h * n_w, C * patch_size * patch_size)
```

### How PyTorch actually implements this

`torch.nn.Unfold(kernel_size=patch_size, stride=patch_size)` is the general-purpose operation this exercise's `patchify` reimplements for the specific non-overlapping case — real ViT implementations usually skip `Unfold` entirely and instead implement patchify-plus-embedding as a single `nn.Conv2d(in_channels, d_model, kernel_size=patch_size, stride=patch_size)`, since a non-overlapping convolution with stride equal to kernel size is mathematically identical to "flatten each patch, then apply the same linear layer to every patch" (this exercise's next question, `02-patch-embedding`) — just computed more efficiently as one convolution instead of an explicit flatten-then-matmul.

## Explanation

`image.reshape(C, n_h, patch_size, n_w, patch_size)` works without rearranging any actual data because `H = n_h * patch_size` and `W = n_w * patch_size` exactly — NumPy's reshape only needs to reinterpret the existing row-major memory layout, splitting the `H` axis into "which row of patches" and "which row within a patch," and the `W` axis analogously. `.transpose(1, 3, 0, 2, 4)` then reorders these five axes so the two grid axes (`n_h`, `n_w`) come first — this is what turns "the same pixel data" into "a grid of patches" as far as the array's logical structure is concerned, since the patch grid axes now vary slowest, matching how a sequence should be ordered. The final `.reshape(n_h * n_w, C * patch_size * patch_size)` flattens the two grid axes together into one sequence axis (row-major, so left-to-right within a row of patches before moving to the next row down), and flattens the remaining `(C, patch_size, patch_size)` axes together into one per-patch vector — exactly the `(num_patches, C*patch_size*patch_size)` shape a transformer's input sequence needs.
