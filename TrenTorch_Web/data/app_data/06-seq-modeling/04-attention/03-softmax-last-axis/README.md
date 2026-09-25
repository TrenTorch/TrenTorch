---
name: seq-attention-softmax-last-axis
title: 'Softmax (reuses Part 1, the first cross-part reuse)'
tags: [transformers]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[01-classical-ml/02-classification/06-softmax-cce]`'s `softmax`, all the way back in this curriculum's very first Part, was written for exactly one shape of input: a `(batch_size, num_classes)` matrix, softmax applied along `axis=1` (each ROW normalized into a probability distribution over classes). `[01-scaled-dot-product-attention]`'s attention scores have a fundamentally different, and more VARIABLE, shape: `(..., seq_len_q, seq_len_k)`, with anywhere from zero to several leading batch and head dimensions depending on the calling context (a single unbatched sequence, a batch of sequences, `[04-multi-head-attention-split]`'s per-head batched computation with an EXTRA head dimension on top of the batch dimension). Softmax always needs to normalize along the LAST axis of whatever that shape happens to be, not a fixed `axis=1`.

Rather than write an entirely new softmax implementation from scratch, this question demonstrates the same reuse-across-parts principle this whole curriculum has built toward, from `[00-math-and-statistics]`'s foundational math questions being reused throughout `[01-classical-ml]`, to `[02-deep-learning-core]`'s autograd engine underlying everything in `[03-dl-training]`, applied here for the FIRST time across an entire Part boundary: Part 1's `softmax`, entirely UNCHANGED, gets reused directly to build this more general version, via a simple reshaping trick rather than any actual reimplementation of the softmax math itself.

### From theory to code

Implement `softmax_last_axis(Z)`. Reshape `Z` (whatever its original rank) down to a 2D array, `(-1, Z.shape[-1])`, collapsing every leading dimension into one, so the LAST axis of the original array becomes exactly `axis=1` of the reshaped 2D array, precisely the axis Part 1's `softmax` already operates on. Call Part 1's `softmax` (already provided, reused via `load_solution`) UNCHANGED on this reshaped 2D array, then reshape the result back to `Z`'s original shape.

### Constraints

- Must call Part 1's `softmax` function DIRECTLY (via the already-provided `softmax_axis1` import), not reimplement the softmax formula independently.
- The reshape-and-reshape-back round trip must preserve the ORIGINAL shape of `Z` exactly, for any rank (2D, 3D, 4D, ...).
- Every "row" along the last axis (in the original, un-reshaped sense) must sum to exactly `1`.

### Hints

<details>
<summary>Hint 1: Reshaping down to 2D</summary>

`Z_2d = Z.reshape(-1, original_shape[-1])`: the `-1` tells NumPy to infer that dimension's size automatically (the product of every OTHER dimension), collapsing all leading dimensions into one, while keeping the LAST dimension exactly as it was.

</details>

<details>
<summary>Hint 2: Calling Part 1's softmax</summary>

`result_2d = softmax_axis1(Z_2d)`, calling the ALREADY-PROVIDED, unmodified Part 1 function directly; `Z_2d` is now genuinely a `(batch_size, num_classes)`-SHAPED array as far as that function is concerned, even though it started life as an attention score tensor.

</details>

<details>
<summary>Hint 3: Reshaping back</summary>

`return result_2d.reshape(original_shape)`, restoring the array to whatever shape `Z` originally had, before the temporary 2D collapse.

</details>

## Theory

### The simple version

Using the exact same measuring tape to measure a room's width regardless of whether the room is a small closet or a large hall, you don't need a DIFFERENT tape for each room size, you just apply the same tool, correctly, to whatever's in front of you. Part 1's `softmax` is the tape; the reshape-to-2D trick is simply ensuring the tape gets applied to the right dimension, no matter how many other dimensions happen to surround it.

### The formula

```
softmax_last_axis(Z):
    Z_2d = Z.reshape(-1, Z.shape[-1])
    result_2d = softmax_axis1(Z_2d)          # Part 1's softmax, UNCHANGED
    return result_2d.reshape(Z.shape)
```

Mathematically, this is EXACTLY the same softmax formula Part 1 already established (`exp(z_i - max(z)) / sum(exp(z_j - max(z)))`), applied independently to every "row" along the last axis; the reshape is purely a BOOKKEEPING device to make Part 1's fixed-axis implementation apply correctly to an array of any rank.

### How PyTorch actually implements this

`torch.nn.functional.softmax(x, dim=-1)` accepts a `dim` argument specifically so it can be applied along ANY axis of a tensor with any rank, exactly the generalization this question builds by hand, and internally, PyTorch's ATen softmax kernel handles arbitrary dimensionality directly rather than needing an explicit reshape trick. This question's reshape-based approach is a genuinely useful and correct technique for exactly this situation: adapting a function that was only ever WRITTEN for a fixed axis convention to a new context with a different shape, without touching or risking breaking the original, already-tested implementation, real production codebases do this kind of "reuse via reshape" constantly when integrating an older utility into a new context with different tensor shapes. `[01-scaled-dot-product-attention]`'s own softmax step could equally have called THIS function instead of computing softmax inline; both are mathematically identical, this question exists specifically to make the cross-Part reuse pattern, and the reshape technique that enables it, explicit and directly testable.

## Explanation

`softmax_last_axis` first records `original_shape = Z.shape`, then reshapes `Z` down to 2D via `Z.reshape(-1, original_shape[-1])`, collapsing every leading dimension into a single "batch" dimension while preserving the last dimension untouched, which is exactly the shape Part 1's `softmax` (fixed to `axis=1`) expects to operate correctly on. It calls that Part 1 function directly, unchanged, on the reshaped array, then reshapes the `(batch, last_dim)`-shaped result back to `original_shape` via `.reshape(original_shape)`, restoring the array's original rank and dimension sizes while the actual softmax values themselves came entirely from Part 1's already-established, tested implementation.
