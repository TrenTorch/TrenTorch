---
name: inf-kv-rope-decoding
title: 'Rotary Position Embeddings at a single decode step'
tags: [inference, rope, positional-encoding, decoding]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Rotary Position Embeddings (RoPE) encode position by rotating each 2D sub-pair of a query/key vector by an angle that grows with position. During training, a whole sequence's rotations are usually applied at once. At inference time, decoding one token at a time, a new token arrives at exactly ONE absolute position (the current cache length) — only that single query/key vector needs to be rotated, not a whole sequence. Implement rotary embeddings applied at a single (or batched) position, the setting that actually matters for autoregressive decoding.

### From theory to code

Implement `apply_rope(x, position, base=10000.0)`:

```
theta_i = base^(-2i/d)                              for i = 0..d/2-1
x'_2i   = x_2i * cos(m*theta_i) - x_2i+1 * sin(m*theta_i)
x'_2i+1 = x_2i * sin(m*theta_i) + x_2i+1 * cos(m*theta_i)
```

### Constraints

- `d` (vector length) must be even.
- `theta_i = base^(-2i/d)` for `i` in `0..d/2-1`.
- Rotate every consecutive pair `(x[2i], x[2i+1])` by angle `position * theta_i`.
- Support batched input of shape `(seq_len, d)` with a matching list/array of positions, and also a single 1D vector with a scalar position.

### Hints

<details>
<summary>Hint: Vectorize with even/odd slicing</summary>

`theta_i` only depends on the pair index `i` and `d`, not on position — compute the theta vector once, then multiply by position `m` to get the per-pair angle. `x[0::2]` and `x[1::2]` give you the two halves of every pair without a Python loop.

</details>

## Theory

### The simple version

Think of each 2D pair of the vector as a tiny clock hand. RoPE spins that hand by an angle proportional to the token's position — token 5's hand is rotated further than token 2's. Two vectors' dot product then naturally depends on the ANGLE BETWEEN their hands, which is exactly their positions' difference, not their absolute positions.

### The formula

```
theta_i = base^(-2i/d),   i = 0..d/2-1
x'_2i   = x_2i*cos(m*theta_i) - x_2i+1*sin(m*theta_i)
x'_2i+1 = x_2i*sin(m*theta_i) + x_2i+1*cos(m*theta_i)
```

Writing each pair as a complex number `z = x_2i + i*x_2i+1`, the update is exactly `z' = z * e^(i*m*theta_i)` — a rotation by angle `m*theta_i`. The dot product of two rotated vectors depends only on their RELATIVE position `m - n`, not on `m` and `n` individually — attention naturally becomes position-relative without a separate relative-position lookup table.

### How PyTorch actually implements this

```python
def apply_rope(x, position, base=10000.0):
    import torch
    single = x.dim() == 1
    if single:
        x, position = x.unsqueeze(0), [position]
    positions = torch.tensor(position, dtype=torch.float32)
    seq_len, d = x.shape
    half = d // 2
    theta = base ** (-2.0 * torch.arange(half) / d)
    angles = positions[:, None] * theta[None, :]
    cos, sin = torch.cos(angles), torch.sin(angles)
    x_even, x_odd = x[:, 0::2], x[:, 1::2]
    out = torch.empty_like(x)
    out[:, 0::2] = x_even * cos - x_odd * sin
    out[:, 1::2] = x_even * sin + x_odd * cos
    return out.squeeze(0) if single else out
```

At inference, RoPE is applied per-token during decoding: each new token comes in at one absolute position `m` (the current cache length), and only that one query/key vector needs to be rotated — much cheaper than recomputing a whole sequence's rotations, and it's why RoPE composes cleanly with a growing KV cache (`[02-autoregressive-decoding-kv-cache]`).

## Explanation

Because rotation by `m*theta_i` then by `-n*theta_i` composes into rotation by `(m-n)*theta_i`, a dot product between a query rotated by `m` and a key rotated by `n` depends only on `m - n` — this relative-position property is exactly why RoPE, unlike a learned absolute position embedding table, generalizes cleanly to positions never seen with that exact absolute value during training (only the relative offsets matter). At position `m=0`, every rotation angle is `0`, so RoPE reduces to the identity transform, which is why the first token in any sequence is always unaffected by it.
