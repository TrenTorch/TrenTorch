---
name: research-lora-param-count
title: 'LoRA: Trainable Parameter Count'
tags: [research-papers, systems, fine-tuning, adapters]
difficulty: Beginner
---

## Statement

### The problem, from first principles

LoRA's appeal is the parameter count. A full weight matrix has d_in times d_out entries; the low-rank update has only r times the sum of the two dimensions.

### From theory to code

Implement `lora_param_count(d_in, d_out, r)`, the trainable parameters of one LoRA adapter.

### Constraints

- Returns an integer.

### Hints

<details>
<summary>Hint 1</summary>

Add the two dimensions and multiply by the rank.

</details>

## Theory

### The simple version

For a 4096 by 4096 layer at rank 8 the adapter has 65,536 parameters, against 16.8 million for the full matrix. That gap is why LoRA fits on modest hardware.

### The formula

$$P_{\text{LoRA}} = r\,(d_{\text{in}} + d_{\text{out}}) \ll d_{\text{in}}\,d_{\text{out}}$$

### How NumPy/PyTorch actually implements this

Fine-tuning reports print this trainable count, which the paper's tables compare against full fine-tuning.

## Explanation

The count is exact for the two factor matrices; there is no bias term in the basic formulation.
