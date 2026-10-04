---
name: lm-dpo-loss
title: Direct Preference Optimization (DPO)
tags: [rlhf, dpo, alignment]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Classic RLHF trains a reward model and then runs reinforcement learning against it while a KL penalty keeps the policy near a reference model. Direct Preference Optimization observes that the optimum of that KL-regularized objective has a closed form: the reward of a response is `beta` times the log-ratio between the policy and the reference. Substituting that reward into the Bradley-Terry likelihood removes the reward model and the reinforcement learning loop. What remains is a logistic loss on the difference of two log-ratios, trained directly on preference pairs with ordinary gradient descent.

### From theory to code

Implement `dpo_implicit_reward` and `dpo_loss`.

### Constraints

- Inputs are summed sequence log-probabilities (one float per response), as NumPy arrays of length `n`: `pi_chosen`, `pi_rejected` from the policy and `ref_chosen`, `ref_rejected` from the frozen reference.
- `dpo_implicit_reward(pi, ref, beta)` is `beta * (pi - ref)`.
- `dpo_loss(pi_chosen, pi_rejected, ref_chosen, ref_rejected, beta)` is the mean of `-log sigmoid(r_chosen - r_rejected)` where each reward is the implicit reward. Use `np.logaddexp(0, -d)`.
- `beta > 0`. Return Python floats.

### Hints

<details>
<summary>Hint 1</summary>

Compute the two implicit rewards, take their difference and reuse the stable logistic loss from the reward-model question.

</details>

<details>
<summary>Hint 2</summary>

If the policy equals the reference both rewards are zero, so the loss must be `ln 2`.

</details>

## Theory

### The simple version

The reference model is an anchor and the policy is a boat tied to it by a rope of length controlled by `beta`. The loss pulls the boat toward responses people preferred and away from the ones they rejected, but it measures progress only as movement relative to the anchor, never in absolute terms.

### The formula

The optimum of $\max_\pi \mathbb{E}[r] - \beta\,\mathrm{KL}(\pi\|\pi_{\text{ref}})$ satisfies $r(x, y) = \beta \ln\frac{\pi(y\mid x)}{\pi_{\text{ref}}(y\mid x)} + \text{const}(x)$. The constant cancels in a pairwise difference, giving

$$
\mathcal{L}_{\text{DPO}} = -\ln \sigma\!\Big(\beta\big[(\ln\pi_c - \ln\pi_{\text{ref},c}) - (\ln\pi_r - \ln\pi_{\text{ref},r})\big]\Big)
$$

### How this is done in practice

TRL's `DPOTrainer` and most open post-training stacks implement this with one forward pass of the policy and one of the frozen reference per response, then cache the reference log-probabilities if memory is tight. The sequence log-probability is the sum of token log-probabilities over the response tokens, built with the masks from the supervised fine-tuning question.

## Explanation

The solution forms the two implicit rewards and passes their difference to a stable logistic loss. Notice what is absent: no reward model, no sampling and no value function. The only extra cost is evaluating the reference model, and the only hyperparameter specific to the method is `beta`, which controls how far the policy is allowed to drift from the reference.
