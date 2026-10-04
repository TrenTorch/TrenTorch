---
name: perf-roofline-model
title: 'Roofline Model'
tags: [performance]
difficulty: Advanced
---

## Statement

Visualize compute vs. memory bound. Optimize code for speed, memory, and energy efficiency.

### Metrics
- Latency (wall-clock time)
- Throughput (operations per second)
- Memory usage (peak and residual)
- Power consumption (watts)

### Hints

<details>
<summary>Hint 1</summary>

Always measure before optimizing. Pick the right metric: latency vs. throughput.

</details>

<details>
<summary>Hint 2</summary>

Profile to find the bottleneck. Don't optimize where the time isn't spent.

</details>

## Theory

### Core Principles

Performance optimization follows these rules:
- Measure first (profiling)
- Identify bottleneck (roofline, critical path)
- Apply optimization to bottleneck
- Re-measure to confirm improvement

### Why it Matters

- 10% speedup on a frequently-called function is worth more than 50% speedup on rarely-called code
- Different hardware has different bottlenecks (CPU, GPU, memory)
- Power consumption is a cost: optimization reduces operational expense

### Real-world constraints

- Trade-offs: speed vs. readability, memory vs. compute
- Hardware evolves (new instructions, cache sizes)
- Profiling overhead affects measurements

## Explanation

The solution measures the system, identifies the bottleneck, applies the optimization, and verifies improvement. Key: understand the roofline (compute-bound vs. memory-bound) before optimizing.

