---
name: numpy-normal-distribution-and-weight-init
title: Normal-Distribution Samples and Weight Initialization
tags: [numpy-random]
difficulty: Intermediate
---

## Statement

Implement functions that draw normally distributed samples, measure their statistics, and use them to initialize a weight matrix.

## Theory

The **normal distribution** is described by mean $\mu$ and standard deviation $\sigma$.

```python
rng.normal(loc=0.0, scale=2.0, size=(3, 4))   # loc = mean, scale = std
rng.standard_normal((3, 4))                    # mean 0, std 1
```

`samples.mean()` and `samples.std()` measure what was actually drawn — close to $\mu$/$\sigma$ but not exact; the gap shrinks as the sample grows, so tests must compare with a tolerance, not exact equality.

**Weight initialization.** A layer's weight matrix has shape `(fan_in, fan_out)`. Weights must not all be the same value (symmetry never breaks) and must not be the wrong scale (values blow up or vanish across layers). **He initialization** draws from a normal distribution with mean $0$ and:

$$
\sigma = \sqrt{\frac{2}{\text{fan\_in}}}
$$

## Explanation

`sample_normal` is `rng.normal(mean, std, shape)`. `empirical_mean_std` returns `(float(samples.mean()), float(samples.std()))` — computed over the flattened array regardless of its original shape, since `.mean()`/`.std()` with no `axis` already aggregate over every element. `he_init` computes `sqrt(2 / fan_in)` with `np.sqrt` and passes it as `scale` to `rng.normal(0.0, scale, (fan_in, fan_out))`.
