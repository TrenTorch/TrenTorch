---
name: research-fsdp-padded-numel
title: 'FSDP: Padded Flat Parameters'
tags: [research-papers, systems, training, sharding]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The flat parameter buffer is padded so every rank holds an equal shard. The padding is at most world minus one elements, which is negligible for large models.

### From theory to code

Implement `fsdp_padded_numel(numel, world)`, the buffer size after padding.

### Constraints

- Return an integer multiple of the world size.

### Hints

<details>
<summary>Hint 1</summary>

Round the shard size up, then multiply back by the world size.

</details>

## Theory

### The simple version

Equal shard sizes keep the all-gather and reduce-scatter calls uniform. Padding costs a few unused elements, which is a fair trade for simpler collectives.

### The formula

$$N_{\text{pad}} = \left\lceil\frac{N}{W}\right\rceil W$$

### How NumPy/PyTorch actually implements this

FSDP pads each flat parameter group to this size before sharding it across ranks.

## Explanation

The padded elements are zeros that never affect the computed gradients, since they are excluded from the real parameter views.
