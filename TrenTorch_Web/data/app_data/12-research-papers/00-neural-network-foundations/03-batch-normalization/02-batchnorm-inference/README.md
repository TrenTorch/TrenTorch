---
name: research-batchnorm-inference
title: 'Batch Normalization: Inference With Running Statistics'
tags: [research-papers, normalization, batchnorm]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Inference runs on one example at a time, so batch statistics are unavailable or unstable. Batch norm instead uses running averages collected during training, fixed at inference time.

### From theory to code

Implement `batchnorm_inference(x, gamma, beta, running_mean, running_var, eps)`, which normalizes with the stored running statistics.

### Constraints

- `running_mean` and `running_var` have shape `(D,)`.
- The output is deterministic for a given input.

### Hints

<details>
<summary>Hint 1</summary>

Use `running_mean` and `running_var` in place of the batch mean and variance, then scale and shift.

</details>

## Theory

### The simple version

Because the statistics are fixed, each example is normalized independently of the rest of the batch. This is why models must be switched to eval mode before inference.

### The formula

$$y = \gamma \frac{x - \mu_{\text{run}}}{\sqrt{\sigma^2_{\text{run}} + \epsilon}} + \beta$$

### How NumPy/PyTorch actually implements this

`model.eval()` makes `torch.nn.BatchNorm1d` use these running buffers instead of batch statistics.

## Explanation

The formula matches training-mode batch norm, with the batch statistics replaced by running estimates. Those estimates are updated by `update_running_stats` in the next question.
