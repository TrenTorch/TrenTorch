---
name: research-zero-shard-size
title: 'ZeRO: The Shard Size'
tags: [research-papers, systems, training, memory]
difficulty: Beginner
---

## Statement

### The problem, from first principles

When parameters are partitioned, each GPU stores a contiguous shard. Every shard should be the same size, so the largest shard is the total divided by the device count, rounded up.

### From theory to code

Implement `shard_size(total, N)`, the ceiling of total over N.

### Constraints

- Uneven totals leave the last shard smaller in practice.

### Hints

<details>
<summary>Hint 1</summary>

Use integer ceiling division.

</details>

## Theory

### The simple version

The per-device memory is set by the largest shard, so the rounding matters for worst-case capacity planning.

### The formula

$$s = \left\lceil \frac{T}{N}\right\rceil$$

### How NumPy/PyTorch actually implements this

FSDP and ZeRO pad flat parameter buffers to this size before sharding.

## Explanation

Padding the total to a multiple of N keeps every shard the same size for collective operations.
