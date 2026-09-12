---
name: inf-attn-scaled-dot-product
title: 'Scaled Dot-Product Attention: the core operation every transformer runs'
tags: [inference, attention, transformers]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every transformer block, in every model, runs the same core operation to decide "which other tokens should this token pay attention to": score a query against a set of keys, turn those scores into a probability distribution, and use that distribution to mix the corresponding values. Given query, key and value matrices for a single attention head, compute this scaled dot-product attention output.

### From theory to code

Implement `scaled_dot_product_attention(Q, K, V, mask=None)`:

```
scores = Q @ K.T
scaled = scores / sqrt(d_k)
scaled[mask == 0] = -inf          # only if mask is given
weights = softmax(scaled, axis=-1)
output = weights @ V
```

### Constraints

- Scale scores by `1/sqrt(d_k)` where `d_k` is the last dimension of `Q` and `K`.
- Apply an additive mask of `-inf` to positions where `mask == 0`, before the softmax, never after.
- Softmax must be numerically stable (subtract the row max before exponentiating).
- Return both the attention output and the attention weight matrix.

### Hints

<details>
<summary>Hint 1: Why the scale factor</summary>

As the head dimension `d_k` grows, `q . k` grows roughly like `d_k` in magnitude for unit-variance inputs. Large-magnitude scores push softmax into a near one-hot regime, which is brittle. Dividing by `sqrt(d_k)` keeps the pre-softmax variance close to 1 regardless of head size.

</details>

<details>
<summary>Hint 2: Masking order matters</summary>

Do the masking on the SCALED logits, before the softmax — never after. Subtract the row-wise max before exponentiating for numerical stability; it doesn't change the softmax result, since softmax is shift-invariant.

</details>

## Theory

### The simple version

Imagine a librarian (the query) looking for a book: they compare their request against every book's label (the keys), get a relevance score per book, turn those scores into a "how much time to spend on each book" split that adds up to 100%, then reads a weighted blend of each book's content (the values) according to that split.

### The formula

```
scores  = Q @ K^T
scaled  = scores / sqrt(d_k)
scaled[mask == 0] = -inf                    # causal / padding mask, optional
weights = softmax(scaled, axis=-1)
output  = weights @ V
```

Causal (autoregressive) decoding must never let position `i` attend to a future position `j > i`. This is enforced by adding `-inf` to the disallowed logits before the softmax, so `exp(-inf) = 0` after normalization — the model literally cannot mix in information from the future.

### How PyTorch actually implements this

```python
import torch, torch.nn.functional as F

def solve(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(-2, -1) / d_k**0.5
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float("-inf"))
    weights = F.softmax(scores, dim=-1)
    return weights @ V, weights
```

`torch.nn.functional.scaled_dot_product_attention` fuses this entire operation (including the numerically-stable softmax and, on supported hardware, a FlashAttention-style memory-efficient kernel) into a single call — the formula above is exactly what it computes.

## Explanation

The row-max subtraction is a shift-invariance property of softmax (`softmax(x) == softmax(x - c)` for any constant `c`), so it changes nothing mathematically while preventing `exp()` overflow for large scores. `-inf` scores exponentiate to exactly `0`, so masked positions receive exactly zero probability mass — this is what makes additive masking (rather than, say, zeroing out weights after the softmax) the correct way to enforce causality: a post-hoc zero-and-renormalize would still let a masked position influence the normalizer during the softmax itself, subtly leaking information about "how many future positions exist," which the `-inf` approach avoids entirely.
