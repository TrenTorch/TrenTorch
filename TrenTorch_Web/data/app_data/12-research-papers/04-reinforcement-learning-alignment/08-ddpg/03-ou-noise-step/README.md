---
name: research-ddpg-ou-step
title: 'DDPG: The Ornstein-Uhlenbeck Exploration Step'
tags: [research-papers, reinforcement-learning, continuous-control, actor-critic]
difficulty: Advanced
---

## Statement

### The problem, from first principles

DDPG explores by adding temporally correlated noise to its actions. The Ornstein-Uhlenbeck process pulls the noise back toward zero while adding fresh random kicks, so consecutive actions are smooth rather than jittery.

### From theory to code

Implement `ou_step(x, theta, sigma, dt, z)`, one Euler step of the Ornstein-Uhlenbeck process with a supplied normal draw.

### Constraints

- Use `sqrt(dt)` for the noise scale.

### Hints

<details>
<summary>Hint 1</summary>

Add the drift `theta * (0 - x) * dt` and the noise `sigma * sqrt(dt) * z` to `x`.

</details>

## Theory

### The simple version

Mean reversion keeps the noise bounded, while the random term keeps it moving. Correlated noise helps physical control tasks, where jerky actions would be harmful.

### The formula

$$x_{t+\Delta} = x_t + \theta(\mu - x_t)\Delta + \sigma\sqrt{\Delta}\,z, \qquad z \sim \mathcal{N}(0,1)$$

### How NumPy/PyTorch actually implements this

Implementations sample `z` from `np.random.normal` each step and add the result to the actor's action.

## Explanation

The update is the Euler-Maruyama discretization of the continuous-time process with mean mu = 0 here.
