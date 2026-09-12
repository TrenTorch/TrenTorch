---
name: inf-quant-roofline
title: 'Prefill and Decode Analysis with the Roofline Model'
tags: [inference, roofline, performance-analysis, prefill, decode]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Whether quantization (or any optimization) actually speeds up a workload depends on whether that workload is compute-bound or memory-bound — optimizing the wrong resource does nothing. Given GPU compute (FLOP/s) and memory bandwidth (bytes/s) specs, and a model/workload's FLOPs and bytes moved, classify a prefill step and a decode step as compute-bound or memory-bound using the roofline model, and estimate each step's wall-clock time.

### From theory to code

```
intensity = flops / bytes_moved
ridge_point = peak_flops_per_sec / peak_bytes_per_sec
time = max(flops / peak_flops_per_sec, bytes_moved / peak_bytes_per_sec)
```

### Constraints

- Compute arithmetic intensity, ridge point, both individual time estimates, the overall predicted time (max of the two), and a `'compute_bound'` vs `'memory_bound'` classification.
- Do this independently for a `'prefill'` step and a `'decode'` step given separately, in one call.
- Handle the edge case `bytes_moved == 0` (pure-compute op, always compute-bound) without dividing by zero.

### Hints

<details>
<summary>Hint: You don't need intensity to get the time right</summary>

Compute both `flops / peak_flops_per_sec` and `bytes_moved / peak_bytes_per_sec` directly — you don't strictly need the intensity/ridge-point comparison to get the right time, but it's the cleanest way to also report WHICH bound is active. The classification is just whichever of the two times is larger.

</details>

## Theory

### The simple version

A kitchen can only cook as fast as its slowest step: either the chef's hands (compute) or how fast ingredients arrive from the pantry (memory bandwidth). If ingredients arrive faster than the chef can use them, the chef is the bottleneck (compute-bound). If the chef sits idle waiting for ingredients, the pantry run is the bottleneck (memory-bound).

### The formula

```
intensity = flops / bytes_moved
ridge_point = peak_flops_per_sec / peak_bytes_per_sec
time = max(flops / peak_flops_per_sec, bytes_moved / peak_bytes_per_sec)
```

This is exactly why LLM **prefill** (many tokens processed in one big batched matmul — high arithmetic intensity, reusing loaded weights across many tokens) tends to be compute-bound, while **decode** (one token at a time — the same weights loaded from memory but reused for far less compute per byte) tends to be memory-bound. This asymmetry is the entire reason techniques like quantization (`[01-symmetric-int8-quantization]` through `[04-blockwise-fp8-quantization]`, all of which move FEWER bytes) and batching (`../04-batching-and-serving-metrics`) target decode specifically.

### How PyTorch actually implements this

This is a scalar performance-modeling calculation with no tensors involved — the same function applies unchanged regardless of which framework produced the flops/bytes estimates being analyzed. Real profiling tools (e.g. NVIDIA's Nsight Compute) report measured arithmetic intensity per kernel and compare it against a GPU's own roofline exactly this way.

## Explanation

Taking the max of `flops/peak_flops_per_sec` and `bytes_moved/peak_bytes_per_sec` directly encodes the roofline model's assumption that the device is limited by whichever resource (compute throughput or memory bandwidth) takes longer to satisfy — comparing intensity to the ridge point is an equivalent, more diagnostic way to express the same comparison, since `ridge_point` is exactly the intensity at which the two times are equal. This is why quantizing weights helps DECODE specifically far more than PREFILL: quantization reduces `bytes_moved` (fewer bytes per weight) without changing `flops`, which only shortens the memory-bound decode step's dominant term — a compute-bound prefill step, whose time is already dominated by `flops/peak_flops_per_sec`, sees little benefit from moving fewer bytes.
