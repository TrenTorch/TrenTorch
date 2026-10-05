---
name: research-lora-delta
title: 'LoRA: The Low-rank Update'
tags: [research-papers, systems, fine-tuning, adapters]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

LoRA (Hu et al., 2021) freezes the pretrained weight and learns only a low-rank update, the product of two thin matrices. Fine-tuning then trains a small fraction of the parameters, and the update can be merged into the weight after training.

### From theory to code

Implement `lora_delta(A, B, alpha, r)`, the scaled low-rank update.

### Constraints

- `B` starts at zero so training begins at the pretrained model.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the up-projection by the down-projection, then scale by alpha over r.

</details>

## Theory

### The simple version

The update has rank at most r, so it can only adjust a low-dimensional subspace of the weight. That limit is what makes the number of trainable parameters small.

### The formula

$$\Delta W = \frac{\alpha}{r}\,BA, \qquad B \in \mathbb{R}^{d_{\text{out}}\times r},\; A \in \mathbb{R}^{r\times d_{\text{in}}}$$

### How NumPy/PyTorch actually implements this

The `peft` library's LoRA layers compute exactly this scaled product and add it to the frozen weight.

## Explanation

Zero-initializing B makes the first forward pass identical to the pretrained model.
