---
name: research-byol-ema-update
title: 'BYOL: The Target Network Update'
tags: [research-papers, unsupervised, self-supervised, bootstrap]
difficulty: Beginner
---

## Statement

### The problem, from first principles

BYOL's target network is not trained by gradients. After every step it moves a small fraction toward the online network, which gives the target a slowly changing, stable identity.

### From theory to code

Implement `ema_update(target, online, tau)`, returning `(1 - tau) * target + tau * online`.

### Constraints

- `tau` is small in practice, such as 0.004 or 0.01.

### Hints

<details>
<summary>Hint 1</summary>

Blend the two parameter arrays with weights `1 - tau` and `tau`.

</details>

## Theory

### The simple version

A slowly moving target gives the online network a consistent regression goal. Without it, the two networks could drift together and collapse to a trivial solution.

### The formula

$$\xi \leftarrow \tau\,\xi + (1 - \tau)\,\theta$$

### How NumPy/PyTorch actually implements this

BYOL implementations apply this update to every target parameter after each optimizer step.

## Explanation

This is the same exponential moving average as in DDPG's soft update; BYOL uses it to make the bootstrap target stable.
