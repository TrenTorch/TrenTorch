---
name: inference-cost-per-inference
title: 'Cost per Inference'
tags: [inference]
difficulty: Advanced
---

## Statement

Optimize dollars spent on inference. Build systems that serve models efficiently at scale.

### Key metrics
- Latency (p50, p99 tail)
- Throughput (requests/second)
- Cost per inference
- GPU utilization

### Hints

<details>
<summary>Hint 1</summary>

What bottleneck limits your system: network, compute, memory?

</details>

<details>
<summary>Hint 2</summary>

How do you measure and optimize each dimension independently?

</details>

## Theory

### Core Principles

Inference optimization is about maximizing throughput while meeting latency SLOs:
- Batching increases GPU utilization
- Caching reduces redundant computation
- Model optimization (quantization, pruning) reduces compute
- Hardware selection (GPU, TPU, CPU) depends on workload

### Why it Matters

- Inference is the expensive part of production ML (training is one-time)
- Cost scales with query volume
- Latency SLO violations degrade user experience
- Efficiency is a competitive moat

### Production constraints

- Heterogeneous queries (batch size varies)
- Strict latency budgets (p99 < 100ms)
- Cost optimization (minimize GPU hours)
- Model updates without downtime

## Explanation

The solution measures current bottlenecks, applies the optimization, and re-measures. Key: understand the binding constraint before optimizing elsewhere.

