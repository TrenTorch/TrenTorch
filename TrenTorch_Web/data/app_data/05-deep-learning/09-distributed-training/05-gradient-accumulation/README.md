---
name: dist-gradient-accumulation
title: 'Gradient Accumulation'
tags: [distributed]
difficulty: Advanced
---

## Statement

Simulate larger batch size. Understand how to train large models across multiple GPUs and machines.

### Key challenges
- Communication overhead (AllReduce, synchronization)
- Load imbalance (some workers slower than others)
- Fault tolerance (any node can fail)
- Debugging (distributed race conditions)

### Hints

<details>
<summary>Hint 1</summary>

Think about what needs to be communicated: gradients, model weights, optimizer state.

</details>

<details>
<summary>Hint 2</summary>

How do you measure efficiency: is it compute, communication, or synchronization?

</details>

## Theory

### Core Principle

Distributed training trades-off complexity for speed. Key trade-offs:
- Data parallelism: simple, all-reduce communication
- Model parallelism: complex, less communication but more coordination
- Pipeline parallelism: best throughput, hard to implement

### Why it Matters

- Training large models (175B params) requires distributed systems
- Training time directly impacts iteration speed (months vs. weeks)
- Communication is often the bottleneck (not compute)
- Efficiency at scale is hard (99% scaling efficiency is good)

### Production challenges

- Heterogeneous hardware (different GPU speeds)
- Network latency between machines
- Dynamic load imbalance
- Silent failures (worker crashes, hangs)

## Explanation

The solution applies the chosen parallelism strategy, measures end-to-end training time, and optimizes for communication efficiency. Key: understand the bottleneck before optimizing elsewhere.

