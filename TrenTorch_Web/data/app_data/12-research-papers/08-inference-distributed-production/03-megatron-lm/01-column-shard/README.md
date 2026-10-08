---
name: research-megatron-column-shard
title: 'Megatron-LM: Column-parallel Weight Shards'
tags: [research-papers, systems, parallelism, training]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Megatron-LM (Shoeybi et al., 2019) splits a large linear layer across GPUs. In the column-parallel case each device holds a block of the output columns, so each computes part of the output independently.

### From theory to code

Implement `column_shard(W, world)`, splitting the weight into one column block per device.

### Constraints

- The output dimension is divisible by the number of devices.

### Hints

<details>
<summary>Hint 1</summary>

Split along the output axis into equal parts.

</details>

## Theory

### The simple version

Each device stores only its share of the weights, which is what lets a layer too large for one GPU fit across several.

### The formula

$$W = [W_1 \mid W_2 \mid \cdots \mid W_p]$$

### How NumPy/PyTorch actually implements this

Megatron's `ColumnParallelLinear` stores exactly this shard on each rank.

## Explanation

The split is along the output columns, so each device's matmul produces a distinct slice of the output.
