---
name: research-ppo-clipped-surrogate
title: 'InstructGPT: The PPO Clipped Objective'
tags: [research-papers, transformers, llm, alignment, rlhf]
difficulty: Advanced
---

## Statement

### The problem, from first principles

InstructGPT was trained with PPO (Schulman et al., 2017). PPO limits how far one update can move the policy, which keeps training stable. The clipped surrogate does this by refusing to reward ratios that leave a small band around 1.

### From theory to code

Implement `clipped_surrogate(ratio, advantage, eps)`, returning the element-wise minimum of the raw and clipped objectives.

### Constraints

- `eps` defaults to 0.2.

### Hints

<details>
<summary>Hint 1</summary>

Compute `ratio * advantage` and `clip(ratio, 1 - eps, 1 + eps) * advantage`, then take `np.minimum`.

</details>

## Theory

### The simple version

For a positive advantage, the objective stops increasing once the ratio passes `1 + eps`. For a negative advantage it stops decreasing once the ratio falls below `1 - eps`. Both prevent overly large updates.

### The formula

$$L^{\text{CLIP}} = \min\big(r_t A_t,\ \operatorname{clip}(r_t, 1-\epsilon, 1+\epsilon)\,A_t\big)$$

### How NumPy/PyTorch actually implements this

PPO implementations in RL libraries compute exactly this per token and average the result across the batch.

## Explanation

The minimum makes the objective pessimistic: it only keeps the clipped branch when clipping removes an incentive to move further.
