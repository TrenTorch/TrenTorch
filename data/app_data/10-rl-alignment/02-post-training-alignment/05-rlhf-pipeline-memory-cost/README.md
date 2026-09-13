---
name: rl-alignment-rlhf-pipeline-memory-cost
title: 'Note: RLHF, the Full Pretrain to SFT to Reward Model to PPO Pipeline'
tags: [reinforcement-learning, nlp, mlops]
difficulty: Beginner
---

## Statement

### The problem, from first principles

This track has built the individual pieces — SFT (`01`), preference data (`03`), a reward model (`04`) — but RLHF is specifically the PIPELINE connecting them: pretrain, then SFT, then train a reward model on preference data, then use PPO to optimize the SFT model against that reward model. Each stage has a genuinely different, quantifiable memory footprint, because PPO in particular needs several full models loaded into memory at once — a real, practical cost that's exactly why DPO (`07`) exists as an alternative.

### From theory to code

Implement `models_required_for_stage` (how many full model copies a given pipeline stage needs simultaneously in memory) and the derived `stage_memory_bytes`, `ppo_memory_multiplier_over_sft`, and `dpo_memory_multiplier_over_ppo`.

### Constraints

- `models_required_for_stage(stage)` returns `1` for `"pretraining"`, `"sft"`, and `"reward_modeling"`; `2` for `"dpo"`; `4` for `"ppo"`. Any other stage name raises `ValueError`.
- `stage_memory_bytes(stage, model_size_bytes)` returns `models_required_for_stage(stage) * model_size_bytes`.
- `ppo_memory_multiplier_over_sft()` returns `4.0`; `dpo_memory_multiplier_over_ppo()` returns `0.5`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

PPO needs FOUR models resident at once: the policy being trained, a FROZEN reference copy of it (to compute a KL penalty against, keeping the policy from drifting too far), the reward model (to score generated responses), and a value model (to estimate the baseline for advantage estimation).

</details>

<details>
<summary>Hint 2</summary>

DPO needs only TWO: the policy being trained, and a frozen reference copy — no reward model, and no value model, because DPO's loss (`07-dpo-direct-preference-optimization`) is computed directly from log-probabilities, with no separate RL rollout loop at all.

</details>

## Theory

### The simple version

Imagine training an athlete for a competition four different ways: (1) just having them practice on their own (pretraining/SFT — one person), (2) also hiring a judge who separately scores their attempts (reward modeling — still basically one "system" being trained at a time), (3) having them practice while ALSO keeping a recording of their OLD form to compare against, hiring the SAME judge to score every attempt live, AND hiring a coach to estimate how good each attempt was BEFORE seeing the judge's score (PPO — four "people" involved simultaneously), versus (4) just directly comparing pairs of past attempts against their old form, no separate judge or coach needed at all (DPO — two "people"). Each stage's very different level of coordination overhead directly translates into very different memory requirements.

### The formula

```text
models_required_for_stage:
    pretraining, sft, reward_modeling = 1     -- one model being trained, nothing else resident
    dpo = 2                                   -- policy + frozen reference policy
    ppo = 4                                   -- policy + frozen reference + reward model + value model

stage_memory_bytes(stage, model_size) = models_required_for_stage(stage) * model_size

ppo_memory_multiplier_over_sft = 4 / 1 = 4.0
dpo_memory_multiplier_over_ppo = 2 / 4 = 0.5
```

This ordering (`pretraining/sft/reward_modeling < dpo < ppo`) reflects a genuine, well-documented practical tradeoff: PPO-based RLHF is the most capable technique in principle (it can incorporate an arbitrary, learned reward signal and iteratively explore), but it's also by far the most memory- and engineering-intensive to run, which is exactly the gap DPO was designed to close.

### How PyTorch actually implements this

Context only, untested by your submission: real RLHF implementations (TRL's `PPOTrainer`, DeepSpeed-Chat, etc.) explicitly load and manage all four of these models simultaneously during PPO training — often across multiple GPUs specifically because a single GPU can't hold four full copies of a large language model at once, which is the real-world manifestation of the `4x` memory multiplier this exercise quantifies directly.

## Explanation

`models_required_for_stage` encodes the pipeline's real structure as a lookup table, one entry per stage, with an explicit `ValueError` for anything not recognized — this exercise's `tests.py` confirms the ordering `pretraining == sft == reward_modeling < dpo < ppo` holds, directly checking the real complexity relationship between stages rather than just individual hardcoded numbers.

`stage_memory_bytes` scales a single model's size by however many copies a stage needs, letting the abstract "4 models" fact translate into a concrete memory number for any given model size.

`ppo_memory_multiplier_over_sft` and `dpo_memory_multiplier_over_ppo` are the two headline numbers this whole exercise is building toward: PPO costs `4x` an ordinary SFT run's memory, and DPO costs exactly `half` of PPO's — a genuine, quantifiable version of the informal claim "DPO is simpler and cheaper than full RLHF" that gets repeated throughout the alignment literature.
