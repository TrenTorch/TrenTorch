---
name: lm-kv-cache-int8
title: INT8 KV-Cache Quantization
tags: [quantization, kv-cache, inference]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

At long context the KV cache, not the weights, dominates memory, and every decoding step reads the whole cache from memory. Storing keys and values as 8-bit integers instead of 16-bit floats halves both the memory and the bandwidth. The cache is quantized on write and dequantized on read. A single scale for the whole tensor would be ruined by one outlier, so the standard choice is a **scale per token and per head**: each `(token, head)` vector of length `d` is divided by its own `absmax / 127`, rounded, and stored as `int8` together with that one float scale.

### From theory to code

Implement `quantize_kv` and `dequantize_kv`.

### Constraints

- `kv` has shape `(T, H, d)`. For every `(t, h)` the scale is `max(|kv[t, h, :]|) / 127`, using scale `1.0` where that maximum is zero.
- `quantize_kv(kv)` returns `(q, scale)` where `q = clip(round(kv / scale), -127, 127)` as `np.int8` (use `np.round`, which rounds halves to even) and `scale` has shape `(T, H)`.
- `dequantize_kv(q, scale)` returns `q * scale[..., None]` as float64.

### Hints

<details>
<summary>Hint 1</summary>

`scale[..., None]` broadcasts over the head dimension.

</details>

<details>
<summary>Hint 2</summary>

The per-vector maximum maps exactly to `+-127`, so the largest element is reproduced without error.

</details>

## Theory

### The simple version

Instead of weighing every parcel on a scale that must handle a truck, each parcel gets a scale suited to its own size. A tiny parcel keeps its precision and a huge one never overflows.

### The formula

$$
s_{t,h} = \frac{\max_i |x_{t,h,i}|}{127}, \qquad q = \text{clip}\big(\text{round}(x / s_{t,h}), -127, 127\big), \qquad \hat x = s_{t,h}\, q
$$

The error per element is at most $s_{t,h}/2$, so the relative error is at most $1/254$ of the vector's largest entry.

### How this is done in practice

vLLM and TensorRT-LLM support INT8 and FP8 KV caches, and the choice of scale granularity (per tensor, per head, per token) trades accuracy for the small overhead of storing scales. Quantizing keys is more sensitive than values because attention scores are exponentiated.

## Explanation

The function is one reduction, one division and one rounding. Storing the scales next to the integers is what makes the cache self-contained, and the error bound in the tests follows directly from rounding to the nearest integer.
