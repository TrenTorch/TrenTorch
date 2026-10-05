---
name: research-fsdp-shard-numel
title: 'FSDP: Elements per Shard'
tags: [research-papers, systems, training, sharding]
difficulty: Beginner
---

## Statement

### The problem, from first principles

PyTorch FSDP (Zhao et al., 2023) shards each group of parameters across ranks in a flat buffer. Every rank stores one equal shard, rounded up so the shards line up across devices.

### From theory to code

Implement `fsdp_shard_numel(numel, world)`, the elements stored per rank.

### Constraints

- Round up.

### Hints

<details>
<summary>Hint 1</summary>

Use integer ceiling division by the world size.

</details>

## Theory

### The simple version

Equal shards let each collective move fixed-size chunks, which keeps communication balanced across ranks.

### The formula

$$s = \left\lceil\frac{n}{W}\right\rceil$$

### How NumPy/PyTorch actually implements this

FSDP's `FlatParameter` computes this shard size when wrapping a module.

## Explanation

The flat buffer is padded to `s * W` elements, the next question's quantity.
