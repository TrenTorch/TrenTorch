---
name: research-reward-pairwise-loss
title: 'InstructGPT: The Pairwise Reward Loss'
tags: [research-papers, transformers, llm, alignment, rlhf]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

InstructGPT (Ouyang et al., 2022) trains a reward model from human rankings. Labelers compare two responses, and the reward model is trained so the preferred response scores higher. The loss only depends on the difference of the two scores.

### From theory to code

Implement `pairwise_reward_loss(r_chosen, r_rejected)`, returning `-log(sigmoid(r_chosen - r_rejected))`.

### Constraints

- Use a numerically stable form such as `logaddexp`.

### Hints

<details>
<summary>Hint 1</summary>

Let `d = r_chosen - r_rejected`. Then `-log(sigmoid(d)) = log(1 + exp(-d))`, which `np.logaddexp(0, -d)` computes safely.

</details>

## Theory

### The simple version

A large positive margin means the model already agrees with the human ranking and the loss is near zero. A reversed margin is penalized roughly linearly.

### The formula

$$\mathcal{L} = -\log \sigma\big(r_\theta(x, y_w) - r_\theta(x, y_l)\big)$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.logsigmoid(r_chosen - r_rejected)` gives the negative of this loss directly.

## Explanation

The Bradley-Terry style form compares only the difference of rewards, so a constant shift in all scores changes nothing.
