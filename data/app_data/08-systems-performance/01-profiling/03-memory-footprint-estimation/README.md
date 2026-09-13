---
name: systems-perf-memory-footprint-estimation
title: Memory Footprint Estimation
tags: [mlops, profiling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-parameter-counting` answers "how many numbers does this model have." That's not yet "will this model fit on my GPU" — the actual memory cost depends on how many _bytes_ each number takes, which depends on precision (`float32` vs `float16` vs `int8`), and on the fact that training needs far more than just the parameters themselves: gradients and optimizer state add up fast.

### From theory to code

Implement `estimate_memory_bytes(params, dtype="float32")`, the raw storage cost of a parameter list at a given precision, and `estimate_optimizer_memory_bytes(params, dtype="float32", optimizer="sgd")`, the full training-time memory cost including gradients and optimizer state.

### Constraints

- `dtype` is one of `"float32"` (4 bytes/element), `"float16"`/`"bfloat16"` (2 bytes/element), `"int8"` (1 byte/element).
- `estimate_memory_bytes` returns total elements times bytes-per-element for the given dtype.
- `estimate_optimizer_memory_bytes` returns parameter bytes + gradient bytes (always equal to parameter bytes) + optimizer state bytes, where optimizer state is `0x` param bytes for `"sgd"`, `1x` for `"momentum"`, `2x` for `"adam"`.
- An empty `params` list returns `0` bytes in both functions.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Reuse the same total-element-count idea as `02-parameter-counting`, then multiply by however many bytes one element of `dtype` takes.

</details>

<details>
<summary>Hint 2</summary>

Every optimizer needs to store a gradient the same size as the parameters it's updating — that's always `1x` extra, regardless of which optimizer. Beyond that, `sgd` needs nothing more, `momentum` needs one more same-sized buffer, `adam` needs two (its first and second moment estimates).

</details>

## Theory

### The simple version

Every weight matrix and bias vector in a network is a fixed-size grid of individually-adjustable numbers, and each of those numbers needs some fixed number of bytes to store, depending on precision — a `float32` number takes 4 bytes, an `int8` number takes just 1. But training needs more than one copy of each number: alongside every parameter sits a gradient of the exact same size, and many optimizers keep one or two more same-sized buffers per parameter to track how that parameter has been updating over time.

### The formula

```text
estimate_memory_bytes(params, dtype) = total_elements * bytes_per_element[dtype]

estimate_optimizer_memory_bytes(params, dtype, optimizer):
    param_bytes = estimate_memory_bytes(params, dtype)
    gradient_bytes = param_bytes                 # always 1x
    optimizer_state_bytes = param_bytes * {sgd: 0, momentum: 1, adam: 2}[optimizer]
    return param_bytes + gradient_bytes + optimizer_state_bytes
```

An Adam-trained `float32` model therefore needs roughly `4x` its raw parameter memory just to hold a single training step's state (params + gradients + two moment estimates) — the concrete, practical reason large models are often trained with `sgd`+momentum or precision tricks (`03-mixed-precision-training`) rather than plain Adam at full precision whenever memory is tight.

### How PyTorch actually implements this

Context only, untested by your submission: `tensor.element_size()` returns exactly the bytes-per-element this exercise hard-codes per dtype (verified in this exercise's own oracle test against real `torch.zeros(1, dtype=...).element_size()` calls), and `torch.optim.Adam`'s internal `state` dict genuinely allocates two extra same-shaped buffers (`exp_avg`, `exp_avg_sq`) per parameter — real, observable GPU memory, not just a theoretical accounting exercise.

## Explanation

`estimate_memory_bytes` sums every array's `.size` (as in `02-parameter-counting`) and multiplies by `_BYTES_PER_DTYPE[dtype]`, a lookup table mapping each supported precision name to its real byte width.

`estimate_optimizer_memory_bytes` computes `param_bytes` once via `estimate_memory_bytes`, treats `gradient_bytes` as always equal to `param_bytes` (a gradient exists for every trainable parameter, at the same shape and dtype), and looks up `optimizer`'s state multiplier (`0` for `sgd`, `1` for `momentum`, `2` for `adam`) to compute `optimizer_state_bytes = param_bytes * multiplier` — the sum of all three is the true memory a training step actually needs, not just the parameters alone.
