---
name: potd-review-model-dropout
title: 'REVIEW MODEL DROPOUT'
tags: [neural-networks]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Neural Networks

---

### Story

Amazon's review-helpfulness classifier uses dropout during training, and because dropout involves
randomness, the mask is given directly rather than generated, so every submission is deterministically
checkable.

---

### The Math

```
out = (x * m) / p_keep
```

where `m` is the given binary mask and `p_keep` is the keep probability (inverted-dropout scaling,
matching a framework's `Dropout` at train time).

### Input Format

```
n p_keep
x_1 ... x_n
m_1 ... m_n
```

`m_i` is `0` or `1`, given directly, not generated.

### Output Format

`out`, `n` values, 6 decimals.

### Constraints

- `1 <= n <= 10^5`, `0 < p_keep <= 1`
- Time limit: 1.0 second.

---

### Example

**Input**

```
4 0.75
1.0 2.0 3.0 4.0
1 0 1 1
```

**Output**

```
1.333333 0.000000 4.000000 5.333333
```

## Theory

### The simple version

Dropout randomly zeroes out some activations during training so the network cannot lean too hard on any single one of them. Scaling the survivors back up keeps the layer's overall output about the same size whether dropout is on or off.

### Inverted dropout scales the survivors up

The surviving (unmasked) activations are divided by `p_keep`, not left as-is: this keeps the
expected value of the layer's output the same whether dropout is applied or not, which is the
entire point of the inverted-dropout convention (it means no rescaling is needed at inference time,
only at train time, when this function runs).

### `p_keep = 1` is the identity

With no dropout at all, every mask entry that could exist is effectively `1`, and dividing by
`p_keep = 1` changes nothing: the output equals the input exactly.

### A dropped unit is exactly zero, regardless of `p_keep`

Where `m_i = 0`, the output is `0.0 / p_keep = 0.0` no matter how small `p_keep` is: a dropped unit
never re-appears because of the scaling. Very small `p_keep` (close to `0.01`) magnifies whatever
survives, which is expected and needs to stay finite and precise, not overflow.

## Explanation

`inverted_dropout` computes `(x * m) / p_keep` as one vectorized expression. Multiplying by the mask
first zeroes out the dropped units unconditionally, then dividing the whole (already-masked) array
by `p_keep` scales only the survivors, since a `0` divided by anything stays `0`. This is exactly
why the multiply has to come before the divide, not the other way around, if `p_keep` were applied
before masking the same result would come out, but only because multiplication and division by a
scalar commute; the important property is that masked entries end up at exactly `0.0`, not some
scaled non-zero residual.
