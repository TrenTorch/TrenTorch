---
name: lm-kl-penalized-rewards
title: KL-Penalized Rewards
tags: [rlhf, kl-divergence, ppo]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

When a language model is optimized against a reward model, it quickly finds responses the reward model loves and humans do not: repetitive, exaggerated or simply gibberish that exploits a flaw. The standard defense is to charge the policy for drifting away from the reference model it started from. The charge is a **KL penalty**, estimated per token from the log-probabilities the two models assign to the sampled tokens. The reward model's score is a single number for the whole response, so it is placed on the last token, while the KL penalty is spread across every token. The result is a per-token reward sequence that a reinforcement learning algorithm can consume.

### From theory to code

Implement `kl_penalized_rewards` and `mean_kl`.

### Constraints

- `logp_policy` and `logp_ref` are `(B, T)` arrays of log-probabilities of the sampled tokens. `lengths` is an integer array of response lengths, with `1 <= lengths[b] <= T`. Tokens at positions `>= lengths[b]` are padding.
- `kl_penalized_rewards(logp_policy, logp_ref, final_reward, lengths, beta)` returns a `(B, T)` array with `-beta * (logp_policy - logp_ref)` at every valid position, plus `final_reward[b]` added at position `lengths[b] - 1`, and exactly `0` at padding.
- `mean_kl(logp_policy, logp_ref, lengths)` is the mean over all valid tokens of `logp_policy - logp_ref`, the simple per-token estimator of the KL divergence from sampled tokens.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Build a valid-token mask from `lengths` with broadcasting, multiply the penalty by the mask, then add the final reward at the last valid index using fancy indexing.

</details>

<details>
<summary>Hint 2</summary>

The expectation of `logp_policy - logp_ref` under tokens sampled from the policy is the KL divergence, which is why this simple difference is a valid estimator.

</details>

## Theory

### The simple version

The reward model is a boss who hands out one bonus at the end of the project. The KL penalty is a running expense report: every step that strays from the agreed procedure costs a little, so wild shortcuts need a big payoff to be worth it.

### The formula

$$
r_t = -\beta\big(\ln\pi_\theta(a_t \mid s_t) - \ln\pi_{\text{ref}}(a_t \mid s_t)\big) + \mathbf{1}[t = T]\, r_{\text{RM}}
$$

Sampling $a_t \sim \pi_\theta$, the average of $\ln\pi_\theta - \ln\pi_{\text{ref}}$ is an unbiased estimate of $\mathrm{KL}(\pi_\theta \,\|\, \pi_{\text{ref}})$ per token.

### How this is done in practice

This is the reward shaping used in the original RLHF and in PPO-based pipelines (TRL's `PPOTrainer`, OpenRLHF). Many systems adapt `beta` to keep the measured KL near a target, and GRPO-style methods move the KL term from the reward into the loss. The estimator here is the simplest one; lower-variance, always non-negative alternatives exist.

## Explanation

The penalty is computed everywhere and zeroed outside the valid region, then the scalar reward is dropped onto the final real token of each row. The mean KL helper reads only valid tokens, so padding never biases the estimate. The two functions together give the reward signal for training and the monitoring number used to decide when the policy has moved too far.
