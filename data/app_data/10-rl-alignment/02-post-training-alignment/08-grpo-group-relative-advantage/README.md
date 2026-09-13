---
name: rl-alignment-grpo-group-relative-advantage
title: 'Note: GRPO, Group-Relative Advantage Without a Value Network'
tags: [reinforcement-learning, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`05-rlhf-pipeline-memory-cost` noted PPO needs a whole extra VALUE model just to estimate a baseline for its advantage calculation — one more full model to train and keep resident in memory. GRPO removes that requirement with a simple idea: sample several responses to the SAME prompt as a "group", score each with the reward model, and use each response's standing RELATIVE to its own group as the advantage — no separate value network needed at all.

### From theory to code

Implement `grpo_group_relative_advantage` (the group-normalized advantage) and `grpo_policy_gradient_loss` (the standard policy-gradient loss, using that advantage).

### Constraints

- `grpo_group_relative_advantage(rewards, eps=1e-8)` returns `(rewards - rewards.mean()) / (rewards.std() + eps)`.
- The result always has mean `0` (up to floating point) regardless of the input rewards' scale or offset.
- `grpo_policy_gradient_loss(log_probs, advantages)` returns `-mean(log_probs * advantages)`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Subtracting the mean centers the rewards around `0` (some end up positive, some negative, relative to the group's average); dividing by the standard deviation then rescales so the SPREAD of advantages is comparable across groups, regardless of whether the raw reward values happened to be tightly clustered or widely spread.

</details>

<details>
<summary>Hint 2</summary>

`grpo_policy_gradient_loss` doesn't care where the advantage came from — it's the exact same "push up log-probability where advantage is positive, push down where negative" formula that any policy-gradient method uses; GRPO's only real innovation is HOW the advantage gets computed.

</details>

## Theory

### The simple version

Imagine grading students not against some fixed external standard, but purely against each other WITHIN the same exam: whoever scores above the class average that day gets positive credit, whoever scores below gets negative credit, and the size of the credit depends on how far above/below the AVERAGE SPREAD of that particular class's scores they landed — a student's own "advantage" is entirely about how they did relative to their specific peer group, recomputed fresh every time. GRPO applies exactly this idea to a language model's sampled responses: no external judge trying to guess an absolute value score in advance (that's what PPO's value network does) — just a direct, cheap comparison within each freshly-sampled group.

### The formula

```text
grpo_group_relative_advantage(rewards) = (rewards - mean(rewards)) / (std(rewards) + eps)

grpo_policy_gradient_loss(log_probs, advantages) = -mean(log_probs * advantages)
```

Because the advantage is always mean-zero within its own group, GRPO trains the policy to push probability mass toward ABOVE-AVERAGE responses and away from BELOW-AVERAGE ones for that specific prompt — with no absolute reward scale to calibrate and no separate value network's predictions to trust (and potentially get wrong).

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact advantage formula from "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models" (Shao et al., 2024), the paper that introduced GRPO — used in DeepSeek's later reasoning models specifically because removing the value network cuts training memory and complexity substantially (echoing `05-rlhf-pipeline-memory-cost`'s theme: fewer simultaneously-resident models is a real, recurring cost-reduction strategy across post-training techniques).

## Explanation

`grpo_group_relative_advantage` mean-centers and then standard-deviation-normalizes the group's rewards — this exercise's `tests.py` confirms the result always has mean `0` and standard deviation close to `1`, that the ordering of rewards within a group is exactly preserved (best reward gets the highest advantage, worst gets the lowest), and — critically — that the NORMALIZATION actually does real work: a tightly-clustered group of rewards and a widely-spread group with the same relative ranking produce advantages of similar MAGNITUDE, not wildly different raw values, which is exactly what dividing by the group's own standard deviation buys you and what a mutant that forgot that division would get wrong.

`grpo_policy_gradient_loss` is the ordinary policy-gradient loss shape, unchanged from any other advantage-based RL method — GRPO's actual contribution is entirely in how the advantage itself gets computed, not in a new loss formula.
