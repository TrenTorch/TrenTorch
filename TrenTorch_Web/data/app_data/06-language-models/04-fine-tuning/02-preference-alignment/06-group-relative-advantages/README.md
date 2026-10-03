---
name: lm-group-relative-advantages
title: GRPO Advantages & Clipped Loss
tags: [rlhf, grpo, policy-gradient]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Policy-gradient methods need an **advantage**: how much better than expected a response was. PPO trains a separate value network to supply the baseline, which doubles the memory of the training job. GRPO removes it with a trick that suits language models: sample a _group_ of `G` responses to the same prompt, score them, and use the group itself as the baseline. A response's advantage is its reward minus the group mean, divided by the group standard deviation. If every response in a group gets the same reward there is nothing to learn from that prompt and the advantage is zero. The advantages then feed the same clipped surrogate used by PPO, which limits how much one update can change the policy.

### From theory to code

Implement `group_advantages` and `clipped_surrogate_loss`.

### Constraints

- `rewards` has shape `(P, G)`: `P` prompts with `G` sampled responses each. `group_advantages(rewards, eps)` returns `(rewards - mean) / (std + eps)` computed per row, with the population standard deviation (`ddof=0`). Use `eps = 1e-6` by default.
- `clipped_surrogate_loss(ratio, advantage, clip_eps)` takes arrays of the same shape, where `ratio = pi_new / pi_old` for each sampled token or response, and returns the mean of `-min(ratio * advantage, clip(ratio, 1 - clip_eps, 1 + clip_eps) * advantage)`.
- A group whose rewards are all equal has advantage exactly 0 for every response.
- Return a `(P, G)` float array and a Python float respectively.

### Hints

<details>
<summary>Hint 1</summary>

Use `keepdims=True` for the mean and standard deviation so they broadcast across the row.

</details>

<details>
<summary>Hint 2</summary>

Compute both candidate terms and take `np.minimum`. The clip bounds how much credit a large ratio can earn when the advantage is positive and how little penalty a small ratio avoids when it is negative.

</details>

## Theory

### The simple version

Ten students answer the same exam question. Instead of comparing each with an abstract passing grade, you grade on a curve within the class: above the class average is good, below is bad, and the spread sets the scale. If all ten give identical answers the curve teaches nothing.

### The formula

$$
A_i = \frac{r_i - \mu_{\text{group}}}{\sigma_{\text{group}} + \epsilon}, \qquad
\mathcal{L} = -\mathbb{E}\Big[\min\big(\rho A,\; \text{clip}(\rho, 1-\varepsilon, 1+\varepsilon)\,A\big)\Big]
$$

with $\rho = \pi_\theta / \pi_{\theta_{\text{old}}}$. With $A>0$ the loss stops rewarding ratios above $1+\varepsilon$, and with $A<0$ it stops rewarding ratios below $1-\varepsilon$.

### How this is done in practice

GRPO was introduced for DeepSeek's reasoning models and is implemented in TRL (`GRPOTrainer`) and most open reinforcement learning stacks for verifiable rewards. Variants differ in details: dividing by the standard deviation or not, normalizing the loss per token or per sequence, and dropping groups with zero variance entirely.

## Explanation

Advantages are computed row-wise with broadcasting. The clipped loss evaluates the unclipped and the clipped objective and takes the elementwise minimum, which is a pessimistic bound: the policy gains nothing from moving outside the trust region and is still punished for moving the wrong way inside it. Together they are the core of a GRPO update without a value network.
