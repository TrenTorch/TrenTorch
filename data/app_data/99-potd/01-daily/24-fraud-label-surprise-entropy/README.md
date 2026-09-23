---
name: potd-fraud-label-surprise-entropy
title: 'THE FRAUD LABEL SURPRISE'
tags: [information-theory]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Information Theory

---

### Story

Stripe's risk team runs a daily check on how "surprising" the label mix looks: entropy near zero
means the day was almost entirely one class, worth a glance before trusting any model metric
computed on it.

---

### The Math

```
H(p) = -sum_i p_i * log2(p_i)
```

### Input Format

```
k
p_1 ... p_k
```

A valid probability distribution, given directly.

### Output Format

`H(p)`, 6 decimals.

### Constraints

- `2 <= k <= 100`, `sum(p_i) = 1` guaranteed within `1e-6`
- Time limit: 1.0 second.

---

### Example

**Input**

```
2
0.995 0.005
```

**Output**

```
0.045415
```

## Theory

### The simple version

Entropy measures how mixed or lopsided a set of probabilities is. A distribution that is almost all one class is unsurprising and has low entropy; one split evenly across many classes is maximally surprising and has high entropy.

### `p_i = 0` contributes exactly `0`, not `NaN`

`0 * log2(0)` is mathematically undefined by direct substitution (`log2(0)` is `-infinity`), but the
standard information-theory convention, justified by the limit `p * log(p) -> 0` as `p -> 0+`, is
that a zero-probability outcome contributes nothing to the entropy. Computing `log2(0)` directly and
multiplying by `0` produces `NaN` in floating point (`0 * -inf`), not `0`, so the zero case needs to
be excluded from the `log` call itself, not just multiplied away afterward.

### Uniform distribution is a clean sanity check

A uniform distribution over `k` classes gives `H = log2(k)` exactly, since every term is
`-(1/k) * log2(1/k) = (1/k) * log2(k)`, and there are `k` of them.

### Many tiny non-zero terms

With `k = 100` and one dominant class, most `p_i` are small but non-zero. Each still needs to be
computed accurately; the risk is not `log(0)` here, it's ordinary floating-point summation over many
small terms, which double precision handles without a special case.

## Explanation

`entropy` masks out the zero probabilities before taking a logarithm at all: it computes
`-p[nonzero] * np.log2(p[nonzero])` only where `p > 0`, and treats every zero-probability entry as
contributing `0.0` directly, rather than computing `log2(0)` and relying on `0 * -inf` to somehow
become `0` (it does not; that expression is `NaN` in IEEE floating point). Summing the per-class
contributions gives `H(p)`.
