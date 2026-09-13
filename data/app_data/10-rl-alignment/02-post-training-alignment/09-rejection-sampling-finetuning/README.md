---
name: rl-alignment-rejection-sampling-finetuning
title: 'Rejection Sampling: Keep Only the Best of Several Sampled Responses'
tags: [reinforcement-learning, nlp]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`04-reward-modeling-bradley-terry` gave us a way to score any individual response — the simplest possible thing to DO with that reward model, before touching PPO or DPO's more sophisticated machinery, is to just sample several candidate responses per prompt, throw away the worse ones, and fine-tune on what's left. This is rejection sampling fine-tuning: no RL loop, no gradient through the reward model at all — just filter, then ordinary SFT (`01-supervised-fine-tuning-response-loss-mask`) on the survivors.

### From theory to code

Implement `filter_top_k_by_reward` (keeping only the best `k` of a sampled group) and `build_rejection_sampling_sft_dataset`, turning many prompts' worth of filtered survivors into one flat SFT-ready dataset.

### Constraints

- `filter_top_k_by_reward(responses, rewards, k)` returns the `k` responses with the highest rewards, best-to-worst.
- `build_rejection_sampling_sft_dataset(prompts, response_groups, reward_groups, k)` applies `filter_top_k_by_reward` independently PER prompt, then returns a flat list of `(prompt, response)` pairs for every survivor.
- `k=0` returns an empty list; `k` equal to a group's full size keeps everything (in some order).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.argsort(-rewards)` sorts indices from HIGHEST reward to lowest (negating flips ascending sort into descending) — the first `k` entries of that order are exactly the ones to keep.

</details>

<details>
<summary>Hint 2</summary>

`build_rejection_sampling_sft_dataset` is just a loop: for each `(prompt, responses, rewards)` triple (zipped together), call `filter_top_k_by_reward`, then append `(prompt, response)` for every survivor.

</details>

## Theory

### The simple version

Imagine a photographer who takes 20 photos of the same scene, then only keeps the 3 best-looking ones and throws the rest away, before showing anyone their portfolio. Rejection sampling for language models is exactly this: sample many candidate responses to the same prompt, use a reward model as the "which ones look good" judge, keep only the best few, and treat those survivors as if they were the ONLY responses ever generated — training on them with completely ordinary supervised fine-tuning.

### The formula

```text
filter_top_k_by_reward(responses, rewards, k):
    order = argsort(-rewards)          -- indices, best reward first
    return [responses[i] for i in order[:k]]

build_rejection_sampling_sft_dataset(prompts, response_groups, reward_groups, k):
    for each (prompt, responses, rewards):
        survivors = filter_top_k_by_reward(responses, rewards, k)
        emit (prompt, response) for every response in survivors
```

The genuinely appealing property of this technique is its simplicity: unlike PPO (`06-ppo-clipped-surrogate-objective`), there's no policy-gradient math, no clipping, no KL penalty — it's ordinary next-token SFT, just on a reward-model-CURATED dataset instead of a human-written one.

### How PyTorch actually implements this

Context only, untested by your submission: this technique (often called "RAFT" — Reward rAnked FineTuning, or the "rejection sampling" step used alongside RLHF in the Llama 2 paper, Touvron et al., 2023) is used in practice specifically because it's dramatically simpler and more stable to implement than full PPO, at the cost of only being able to improve toward responses the base model could already generate SOME of the time (unlike PPO, which can in principle discover genuinely novel high-reward behavior through exploration).

## Explanation

`filter_top_k_by_reward` sorts a group's indices by descending reward and slices off the top `k` — this exercise's `tests.py` confirms the survivors come back in best-to-worst order, that `k` equal to the group size keeps everyone, and that ties in reward don't crash or silently drop responses.

`build_rejection_sampling_sft_dataset` applies this filtering independently to each prompt's own group of sampled responses (never mixing responses across different prompts), then flattens every survivor back into a `(prompt, response)` pair — exactly the shape `02-instruction-vs-pretraining-datasets`'s `build_instruction_example` expects as its input, making the connection to ordinary SFT concrete: rejection sampling only changes WHICH data gets trained on, not the training procedure itself.
