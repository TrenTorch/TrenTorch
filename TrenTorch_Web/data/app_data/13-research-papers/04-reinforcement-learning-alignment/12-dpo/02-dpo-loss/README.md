---
name: research-dpo-loss
title: 'DPO: The Preference Loss'
tags: [research-papers, reinforcement-learning, alignment, dpo]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The DPO loss is a logistic loss on the implicit reward margin. It is the same as the reward-model loss from the reward-modelling question, but applied directly to the policy's log-probabilities.

### From theory to code

Implement `dpo_loss(logit)`, returning `-log(sigmoid(logit))` in a numerically stable form.

### Constraints

- Use `logaddexp` to avoid overflow for large magnitudes.

### Hints

<details>
<summary>Hint 1</summary>

The loss equals `log(1 + exp(-logit))`, which `np.logaddexp(0, -logit)` computes safely.

</details>

## Theory

### The simple version

The loss falls toward zero as the margin grows positive, and rises linearly for negative margins. Gradient descent therefore widens the gap between the preferred and dispreferred responses.

### The formula

$$\mathcal{L}_{\text{DPO}} = -\log\sigma(z) = -\log\sigma\!\left(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta\log\frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)$$

### How NumPy/PyTorch actually implements this

The DPO trainer calls `F.logsigmoid` on the margin, which is the same stable computation.

## Explanation

Writing the loss as logaddexp avoids computing exp of large positive numbers, which matters when margins are big.
