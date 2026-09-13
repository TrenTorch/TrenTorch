---
name: rl-alignment-reward-modeling-bradley-terry
title: 'Reward Modeling: Training a Model to Score a Response Instead of Generate One'
tags: [reinforcement-learning, nlp, neural-networks]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`03-preference-datasets-chosen-rejected` gave us pairs of (chosen, rejected) responses to the same prompt — but a preference PAIR isn't directly useful for guiding generation; what's needed is a single SCALAR reward function that can score any individual response on its own, so PPO (`06-ppo-clipped-surrogate-objective`) or best-of-N (`10-best-of-n-sampling`) can optimize against it. A reward model is exactly that: the same architecture as a language model, but repurposed to output one number instead of a next-token distribution.

### From theory to code

Implement `pooled_last_token_representation` (summarizing a whole response into one vector), `reward_model_score` (a linear "reward head" mapping that vector to a scalar), and `reward_model_loss`, the real Bradley-Terry pairwise preference loss used to train reward models in RLHF.

### Constraints

- `pooled_last_token_representation(hidden_states, seq_len)` returns `hidden_states[seq_len - 1]` — the LAST real (non-padding) token's hidden state.
- `reward_model_score(pooled_representation, reward_head_weight, reward_head_bias)` applies `01-hypothesis-function`'s `linear` and returns a plain Python `float`.
- `reward_model_loss(chosen_reward, rejected_reward)` returns `-log(sigmoid(chosen_reward - rejected_reward))` — low when `chosen_reward > rejected_reward`, high when it's backwards.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

By the time a causal transformer reaches the LAST token of a sequence, its hidden state has (via attention) already incorporated information from every earlier token — that's exactly why pooling just the last token's hidden state is enough to summarize the whole response.

</details>

<details>
<summary>Hint 2</summary>

`reward_model_loss` is the exact same shape as `07-dpo-direct-preference-optimization`'s loss — both are Bradley-Terry pairwise comparisons, `-log(sigmoid(difference))` — just applied to different quantities (a reward model's raw scalar scores here, versus DPO's implicit log-probability-ratio margin there).

</details>

## Theory

### The simple version

Imagine training a judge (rather than a contestant) for a cooking competition: instead of teaching someone to COOK a dish, you teach them to look at any finished dish and assign it a single quality SCORE — and the way you train that judging skill is by repeatedly showing them two dishes at a time and having them learn to score the one a human preferred higher than the other. A reward model is exactly this judge: given `03-preference-datasets-chosen-rejected`'s (chosen, rejected) pairs, it learns to assign the chosen response a higher scalar score than the rejected one, without ever being told the "correct" absolute score for either.

### The formula

```text
pooled_last_token_representation(hidden_states, seq_len) = hidden_states[seq_len - 1]

reward_model_score(pooled, W, b) = linear(pooled, W, b)   -- W has shape (1, hidden_dim), a single output "reward" unit

reward_model_loss(chosen_reward, rejected_reward) = -log(sigmoid(chosen_reward - rejected_reward))
```

This loss comes directly from the Bradley-Terry model of pairwise comparisons: it interprets `sigmoid(chosen_reward - rejected_reward)` as the PROBABILITY that a human would prefer the chosen response, and trains the reward model to make that probability as close to `1` (certainty) as possible for every real preference pair in the training data.

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact loss function from the InstructGPT paper (Ouyang et al., 2022), which trains a reward model by taking a pretrained language model, replacing its final vocabulary-sized output layer with a single linear unit (exactly `reward_model_score`'s "reward head"), and training on human preference comparisons with this Bradley-Terry loss — the resulting reward model is then what PPO (`06-ppo-clipped-surrogate-objective`) optimizes against in the full RLHF pipeline (`05-rlhf-pipeline-memory-cost`).

## Explanation

`pooled_last_token_representation` simply indexes the hidden-state sequence at its last real position — `tests.py` confirms it correctly ignores any padding that comes after that position, rather than blindly taking the last row of the full (possibly padded) tensor.

`reward_model_score` reuses the existing `linear` function with a single-output weight matrix, and `.item()`s the result down to a plain scalar — a reward model's whole job is producing exactly one number per response, unlike a language model's per-position vocabulary distribution.

`reward_model_loss` implements the Bradley-Terry formula directly, and this exercise's `tests.py` confirms the loss decreases as the reward gap between chosen and rejected grows in the CORRECT direction (chosen higher), increases when it's backwards, and matches the formula computed independently term-by-term — ruling out a version that accidentally swaps which reward is subtracted from which, which would silently train the reward model to prefer the WORSE response.
