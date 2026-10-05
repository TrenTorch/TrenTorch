---
name: research-dpo-logit
title: 'DPO: The Implicit Reward Margin'
tags: [research-papers, reinforcement-learning, alignment, dpo]
difficulty: Advanced
---

## Statement

### The problem, from first principles

DPO (Rafailov et al., 2023) skips the reward model and the RL loop. It shows that the optimal policy under a KL-constrained reward has an implicit reward, beta times the log-ratio against the reference. Preferences can then be learned directly from that margin.

### From theory to code

Implement `dpo_logit(logp_w, logp_l, ref_w, ref_l, beta)`, returning beta times the difference of the two log-ratios.

### Constraints

- Both log-ratios are taken against the same reference model.

### Hints

<details>
<summary>Hint 1</summary>

Compute the winner's log-ratio minus the loser's, then multiply by beta.

</details>

## Theory

### The simple version

The margin is positive when the policy prefers the winner more than the reference does. Training pushes that margin up, which is exactly what the preference data asks for.

### The formula

$$z = \beta\Big[\log\frac{\pi_\theta(y_w\mid x)}{\pi_{\text{ref}}(y_w\mid x)} - \log\frac{\pi_\theta(y_l\mid x)}{\pi_{\text{ref}}(y_l\mid x)}\Big]$$

### How NumPy/PyTorch actually implements this

The DPO trainer in TRL forms this margin from the policy and reference log-probabilities computed on the same batch.

## Explanation

The reference terms cancel the model's default preferences, so the margin measures only what preference training has added.
