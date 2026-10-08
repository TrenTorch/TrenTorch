---
name: research-ddpg-soft-update
title: 'DDPG: Soft Target Updates'
tags: [research-papers, reinforcement-learning, continuous-control, actor-critic]
difficulty: Beginner
---

## Statement

### The problem, from first principles

DDPG (Lillicrap et al., 2015) keeps slowly moving target networks for stability. Instead of copying the online weights every so often, the target takes a small step toward them after every update.

### From theory to code

Implement `soft_update(target, online, tau)`, returning the blended parameters.

### Constraints

- `tau` is small in practice, such as 0.001.

### Hints

<details>
<summary>Hint 1</summary>

Blend the target and online arrays with weights `1 - tau` and `tau`.

</details>

## Theory

### The simple version

A small tau keeps the bootstrap target nearly fixed for many steps, which damps the feedback loop between the critic and its own targets.

### The formula

$$\theta' \leftarrow \tau\,\theta + (1 - \tau)\,\theta'$$

### How NumPy/PyTorch actually implements this

Deep RL libraries apply this update to every parameter pair after each optimizer step.

## Explanation

This is an exponential moving average of the online parameters, with time constant about 1 / tau updates.
