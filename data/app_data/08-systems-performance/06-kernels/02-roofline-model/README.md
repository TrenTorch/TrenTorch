---
name: systems-perf-roofline-model
title: 'Memory-Bound vs Compute-Bound: The Roofline Model, Why Fusion Helps One but Not the Other'
tags: [mlops, kernels]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-kernel-fusion` showed fusion cuts memory traffic dramatically. That's not automatically the same thing as "makes the computation faster" — a computation's actual speed is limited by whichever resource (compute throughput or memory bandwidth) it exhausts first, and cutting memory traffic only helps when memory bandwidth was the actual bottleneck to begin with.

### From theory to code

Implement `arithmetic_intensity(flops, bytes_moved)`, `ridge_point(peak_flops_per_sec, peak_bytes_per_sec)`, `is_memory_bound(...)`, and `achievable_flops_per_sec(...)` — together, the classic "roofline model" for predicting a computation's actual achievable throughput on given hardware.

### Constraints

- `arithmetic_intensity` returns `flops / bytes_moved` (FLOPs per byte of memory traffic).
- `ridge_point` returns `peak_flops_per_sec / peak_bytes_per_sec` — the intensity at which compute and memory bandwidth saturate simultaneously.
- `is_memory_bound` returns `True` iff the computation's own intensity is _strictly below_ the hardware's ridge point.
- `achievable_flops_per_sec` returns `min(peak_flops_per_sec, arithmetic_intensity * peak_bytes_per_sec)`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Both `arithmetic_intensity` and `ridge_point` are simple ratios — `flops/bytes_moved` for one, `peak_compute/peak_bandwidth` for the other. Comparing the two ratios directly tells you which resource runs out first.

</details>

<details>
<summary>Hint 2</summary>

`achievable_flops_per_sec` is a `min` of two competing ceilings: the hardware's raw compute ceiling (`peak_flops_per_sec`), and what the memory system can actually _feed_ the compute units at this intensity (`arithmetic_intensity * peak_bytes_per_sec`) — whichever is smaller is the real bottleneck.

</details>

## Theory

### The simple version

Imagine a factory where raw materials arrive by truck and get turned into finished goods on an assembly line. If trucks can't deliver materials fast enough, the assembly line sits idle waiting — the factory's output is limited by delivery speed, no matter how fast the line itself could theoretically run (**memory-bound**). If trucks are delivering plenty fast and the assembly line itself is the slow part, more trucks won't help at all — output is limited by the line's own processing speed (**compute-bound**). The roofline model is exactly this observation, formalized: a computation's real throughput is whichever ceiling — delivery rate or processing rate — it hits first.

### The formula

```text
arithmetic_intensity = flops / bytes_moved
ridge_point           = peak_flops_per_sec / peak_bytes_per_sec

is_memory_bound        = arithmetic_intensity < ridge_point
achievable_flops_per_sec = min(peak_flops_per_sec, arithmetic_intensity * peak_bytes_per_sec)
```

This is exactly why `01-kernel-fusion` "helps one but not the other": fusion reduces `bytes_moved` for the same `flops`, which _increases_ `arithmetic_intensity`. For a memory-bound computation (low intensity, below the ridge point), that increase directly raises the achievable throughput — the delivery trucks are now carrying more useful cargo per trip. For an already compute-bound computation (intensity already above the ridge point), throughput is already capped at `peak_flops_per_sec` regardless of intensity — the assembly line was already the bottleneck, so faster delivery changes nothing.

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact roofline model published in Williams, Waterman & Patterson's "Roofline: An Insightful Visual Performance Model for Multicore Architectures" (2009) — verified directly in this exercise's own `tests.py` against that published formula. Real GPU profiling tools (NVIDIA's Nsight Compute among them) plot exactly this roofline chart for real kernels, which is how engineers decide whether a given operation is even worth trying to fuse or optimize further — an operation that's already compute-bound gains nothing from memory-traffic optimizations like fusion, and effort is better spent elsewhere.

## Explanation

`arithmetic_intensity` and `ridge_point` are both plain division — the former describes a specific computation's own FLOPs-per-byte, the latter describes a piece of hardware's own compute-to-bandwidth ratio, and comparing them (`is_memory_bound`) is what tells you which side of the "roofline" this particular computation, on this particular hardware, actually falls on.

`achievable_flops_per_sec` takes the `min` of the hardware's flat compute ceiling and the sloped, intensity-dependent memory ceiling (`arithmetic_intensity * peak_bytes_per_sec`) — below the ridge point, the sloped memory ceiling is lower and wins; at or above it, the flat compute ceiling is lower and wins. This single `min` expression is the entire roofline model's predictive content: it tells you exactly what throughput to expect, and exactly which lever (more bandwidth, or more raw compute) would actually move that number.
