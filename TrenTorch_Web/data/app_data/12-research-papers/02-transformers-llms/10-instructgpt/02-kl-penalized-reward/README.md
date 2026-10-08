---
name: research-kl-penalized-reward
title: 'InstructGPT: The KL-Penalized Reward'
tags: [research-papers, transformers, llm, alignment, rlhf]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Optimizing a reward model alone makes the policy drift into strange outputs that exploit the reward. InstructGPT keeps the policy close to the supervised model by subtracting a penalty for how far its log-probabilities move from the reference.

### From theory to code

Implement `kl_penalized_reward(reward, logp_policy, logp_ref, beta)`, which subtracts `beta` times the log-probability difference from the reward.

### Constraints

- Positive `logp_policy - logp_ref` means the policy has moved toward the response.

### Hints

<details>
<summary>Hint 1</summary>

The penalty is `beta * (logp_policy - logp_ref)`; subtract it from the reward.

</details>

## Theory

### The simple version

The log-ratio is a per-sample estimate of how much the policy has changed from the reference. Penalizing it keeps the policy from chasing high reward at the cost of fluency.

### The formula

$$r'(x, y) = r_\theta(x, y) - \beta\,\log\frac{\pi_\theta(y \mid x)}{\pi_{\text{ref}}(y \mid x)}$$

### How NumPy/PyTorch actually implements this

RLHF trainers compute this penalty per token or per sequence before the policy-gradient update.

## Explanation

The penalty is a sampled version of the KL divergence between the policy and the reference, so it is cheap to compute from log-probabilities.
