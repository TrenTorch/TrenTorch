---
name: research-fsdp-memory-per-rank
title: 'FSDP: Memory per Rank'
tags: [research-papers, systems, training, sharding]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Sharding is the point of FSDP: each rank holds only its portion of the parameters. The memory per rank falls roughly as one over the world size.

### From theory to code

Implement `fsdp_memory_per_rank(numel, world, nbytes)`, the bytes of one rank's shard.

### Constraints

- Returns an integer.

### Hints

<details>
<summary>Hint 1</summary>

Compute the shard size and multiply by bytes per element.

</details>

## Theory

### The simple version

Full materialization happens only for the layer being computed, so peak memory is the shard plus one unsharded layer, not the whole model.

### The formula

$$M_{\text{rank}} = \left\lceil\frac{N}{W}\right\rceil b$$

### How NumPy/PyTorch actually implements this

Memory profilers report the sharded buffer size per rank, which this formula predicts.

## Explanation

The rounding up is the padding cost; it is small when the parameter count is large.
