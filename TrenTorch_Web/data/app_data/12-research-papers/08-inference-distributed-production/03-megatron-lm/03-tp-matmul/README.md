---
name: research-megatron-tp-matmul
title: 'Megatron-LM: Tensor-parallel Matrix Multiply'
tags: [research-papers, systems, parallelism, training]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Column-parallel matrix multiplication gives the same result as the dense product. Each device computes its own output columns from the replicated input, and concatenating those columns reproduces the full output without communication.

### From theory to code

Implement `tensor_parallel_matmul(x, shards)`, multiplying by each column shard and concatenating.

### Constraints

- The input is the same on every device.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the input by each shard, then concatenate the outputs along the feature axis.

</details>

## Theory

### The simple version

Because no partial sums are needed here, column parallelism needs no communication in the forward pass. Row parallelism, the partner layer, adds the all-reduce.

### The formula

$$xW = x\,[W_1 \mid \cdots \mid W_p] = [\,xW_1 \mid \cdots \mid xW_p\,]$$

### How NumPy/PyTorch actually implements this

Megatron MLP blocks pair one column-parallel and one row-parallel matmul, the structure this question checks.

## Explanation

The identity is exact: concatenating column blocks of a product is the product with the column-blocked matrix.
