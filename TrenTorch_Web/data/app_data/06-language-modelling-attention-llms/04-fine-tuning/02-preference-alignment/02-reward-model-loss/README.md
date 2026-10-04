---
name: lm-reward-model-loss
title: Reward Modeling
tags: [rlhf, reward-model, bradley-terry]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

People are bad at assigning a score to a response but good at saying which of two responses is better. A reward model is trained from exactly that kind of data: pairs of a **chosen** and a **rejected** response to the same prompt. The Bradley-Terry model says the probability that the chosen response wins is a logistic function of the difference between their scalar rewards. Training maximizes the likelihood of the observed choices. Only the difference matters, so the reward scale and offset are arbitrary, which is why reward models are often normalized before use.

### From theory to code

Implement `reward_model_loss(r_chosen, r_rejected)` and `preference_accuracy(r_chosen, r_rejected)`.

### Constraints

- `r_chosen` and `r_rejected` are float arrays of length `n`, the scalar reward of each response in each pair.
- `reward_model_loss` returns the mean of `-log sigmoid(r_chosen - r_rejected)`. It must be stable for differences of magnitude 1000: use `np.logaddexp(0, -d)`.
- `preference_accuracy` returns the fraction of pairs with `r_chosen > r_rejected`. Ties count as incorrect.
- Both return Python floats.

### Hints

<details>
<summary>Hint 1</summary>

`-log sigmoid(d) = log(1 + exp(-d)) = np.logaddexp(0, -d)`, which avoids overflow for very negative `d`.

</details>

<details>
<summary>Hint 2</summary>

When `d = 0` the loss is `ln 2`, the value of a model that has no opinion.

</details>

## Theory

### The simple version

A chess ladder works the same way. Nobody measures a player's strength directly. Matches between pairs produce wins and losses, and the ratings are whatever numbers make those outcomes most likely. A bigger rating gap means a more predictable result.

### The formula

$$
P(\text{chosen} \succ \text{rejected}) = \sigma(r_c - r_r), \qquad
\mathcal{L} = -\frac{1}{n}\sum_i \ln \sigma\!\left(r_c^{(i)} - r_r^{(i)}\right)
$$

The gradient with respect to the difference $d$ is $-\sigma(-d)$: a pair the model already ranks correctly contributes almost nothing and a confidently wrong pair contributes a gradient near $-1$.

### How this is done in practice

A real reward model is a language model with its output head replaced by a single scalar read from the final token, trained with this exact loss on human or AI preference pairs. Libraries such as TRL provide `RewardTrainer`. The scores are only meaningful relative to each other, so deployed pipelines often whiten them or subtract a running mean before using them for reinforcement learning.

## Explanation

The loss is a stable logistic loss on the reward difference, and accuracy simply checks the sign. Using `logaddexp` is the important numerical detail: computing `sigmoid` first and then taking a log underflows to `log(0)` for confident, correct predictions with large negative differences in the other direction.
