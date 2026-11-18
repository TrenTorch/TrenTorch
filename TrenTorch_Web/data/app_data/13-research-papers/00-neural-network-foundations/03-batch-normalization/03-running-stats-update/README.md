---
name: research-batchnorm-running-stats
title: 'Batch Normalization: Updating Running Statistics'
tags: [research-papers, normalization, batchnorm]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Inference needs stable statistics, but a single batch is noisy. The paper (and later practice) tracks an exponential moving average of batch means and variances over training, updated after each batch.

### From theory to code

Implement `update_running_stats(running_mean, running_var, batch_mean, batch_var, momentum)`, which returns the updated running mean and variance.

### Constraints

- `momentum` is in `[0, 1]`; the default is `0.1`.

### Hints

<details>
<summary>Hint 1</summary>

Blend the old value with the new one: `(1 - momentum) * old + momentum * new`, for both mean and variance.

</details>

## Theory

### The simple version

A moving average smooths out batch-to-batch noise. A small momentum gives a long memory of past batches; momentum 1 keeps only the newest batch.

### The formula

$$\mu_{\text{run}} \leftarrow (1 - \alpha)\,\mu_{\text{run}} + \alpha\,\mu_B, \qquad \sigma^2_{\text{run}} \leftarrow (1 - \alpha)\,\sigma^2_{\text{run}} + \alpha\,\sigma^2_B$$

### How NumPy/PyTorch actually implements this

`torch.nn.BatchNorm1d` updates `running_mean` and `running_var` with exactly this rule using `momentum=0.1` by default.

## Explanation

The update uses the same blending for mean and variance, with `alpha` as the momentum. Returning new arrays keeps the caller in control of state.
