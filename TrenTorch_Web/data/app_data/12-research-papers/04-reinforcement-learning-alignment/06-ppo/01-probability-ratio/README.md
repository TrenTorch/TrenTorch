---
name: research-ppo-probability-ratio
title: 'PPO: The Probability Ratio'
tags: [research-papers, reinforcement-learning, policy-gradient, ppo]
difficulty: Beginner
---

## Statement

### The problem, from first principles

PPO (Schulman et al., 2017) reuses each batch of experience for several updates. To do that correctly, each sample is reweighted by how much more or less likely the current policy is to take its action than the policy that collected it.

### From theory to code

Implement `probability_ratio(logp_new, logp_old)`, returning `exp(logp_new - logp_old)`.

### Constraints

- Work in log space; exponentiate the difference.

### Hints

<details>
<summary>Hint 1</summary>

Subtract the log-probabilities, then take `exp`.

</details>

## Theory

### The simple version

Computing the ratio through logs avoids multiplying tiny probabilities, which would underflow for long action sequences.

### The formula

$$r_t(\theta) = \frac{\pi_\theta(a_t\mid s_t)}{\pi_{\theta_{\text{old}}}(a_t\mid s_t)} = \exp\big(\log\pi_\theta - \log\pi_{\theta_{\text{old}}}\big)$$

### How NumPy/PyTorch actually implements this

PPO implementations compute `torch.exp(new_logp - old_logp)` on the stored log-probabilities.

## Explanation

The ratio is one at the start of each update and drifts as the policy changes, which is what the clipping later constrains.
