---
name: research-zero-partition-bounds
title: 'ZeRO: Partition Bounds'
tags: [research-papers, systems, training, memory]
difficulty: Advanced
---

## Statement

### The problem, from first principles

ZeRO assigns each device a slice of the flattened parameters. Each device needs to know exactly which elements it owns, which is the start and end of its contiguous range.

### From theory to code

Implement `partition_bounds(total, N, rank)`, returning the half-open range of elements for one device.

### Constraints

- Shard sizes differ by at most one.

### Hints

<details>
<summary>Hint 1</summary>

Compute the sizes of all shards with the array-split rule, sum the sizes before this rank for its start, then add its size.

</details>

## Theory

### The simple version

Contiguous, near-equal shards make the all-gather and reduce-scatter collectives simple to implement with plain offsets.

### The formula

$$\text{start}_r = \sum_{i<r} s_i, \qquad \text{end}_r = \text{start}_r + s_r$$

### How NumPy/PyTorch actually implements this

Sharded optimizers compute these offsets to slice their flat state tensors.

## Explanation

The `array_split` rule gives the first few shards one extra element when the total does not divide evenly.
