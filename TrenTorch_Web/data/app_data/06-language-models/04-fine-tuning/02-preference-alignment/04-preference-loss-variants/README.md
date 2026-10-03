---
name: lm-preference-loss-variants
title: Preference Loss Variants: IPO & SimPO
tags: [rlhf, dpo, alignment]
difficulty: Advanced
---

## Statement

### The problem, from first principles

DPO has two known weak points. Its logistic loss keeps rewarding larger margins forever, so on clean data it can push the policy far from the reference and overfit. And it needs a reference model and the log-ratio, which costs memory and ties the training signal to a quantity that does not match what the model is judged on at generation time. Two variants repair one thing each. **IPO** replaces the logistic loss with a squared error towards a fixed target margin, so the margin is regularized instead of maximized. **SimPO** drops the reference model, uses the _average_ token log-probability so that response length cannot be exploited, and adds a margin `gamma` that the winner must beat the loser by.

### From theory to code

Implement `ipo_loss` and `simpo_loss`.

### Constraints

- `ipo_loss(pi_chosen, pi_rejected, ref_chosen, ref_rejected, tau)` is the mean of `(h - 1 / (2 * tau)) ** 2` where `h = (pi_chosen - ref_chosen) - (pi_rejected - ref_rejected)`. Inputs are summed sequence log-probabilities.
- `simpo_loss(pi_chosen, pi_rejected, len_chosen, len_rejected, beta, gamma)` is the mean of `-log sigmoid(beta * (pi_chosen / len_chosen - pi_rejected / len_rejected) - gamma)`. Use `np.logaddexp(0, -z)`.
- SimPO uses no reference model. `len_*` are the response token counts, positive integers.
- `tau > 0`, `beta > 0`, `gamma >= 0`. Return Python floats.

### Hints

<details>
<summary>Hint 1</summary>

For IPO the minimum is exactly at `h = 1 / (2 tau)`, so a margin that is too large is penalized as well.

</details>

<details>
<summary>Hint 2</summary>

For SimPO normalize each response by its own length before taking the difference, then subtract `gamma` inside the sigmoid.

</details>

## Theory

### The simple version

DPO says "be as different from the loser as you can". IPO says "be better than the loser by about this much, and stop". SimPO says "judge the responses the way you will generate them, per token, and demand a clear gap".

### The formula

$$
\mathcal{L}_{\text{IPO}} = \Big(h - \tfrac{1}{2\tau}\Big)^2, \qquad
\mathcal{L}_{\text{SimPO}} = -\ln \sigma\!\Big(\beta\big[\tfrac{\ln \pi_c}{|y_c|} - \tfrac{\ln \pi_r}{|y_r|}\big] - \gamma\Big)
$$

where $h$ is the DPO log-ratio difference without the $\beta$ scale. The IPO loss is quadratic, so its gradient shrinks to zero at the target and never explodes on separable data.

### How this is done in practice

TRL exposes both through `DPOTrainer` loss options (`loss_type="ipo"` and a dedicated `CPOTrainer`/SimPO configuration). Newer methods such as KTO and ORPO follow the same pattern: change the shape of the loss on the log-ratio, or remove the reference model, to trade off stability, memory and sensitivity to noisy labels.

## Explanation

IPO is a single squared term around a fixed target, and SimPO is DPO's logistic loss with two edits: the average log-probability replaces the summed one and the reference log-ratio is replaced by a plain margin. Length normalization means that a long, rambling answer cannot gain reward just from having more tokens.
