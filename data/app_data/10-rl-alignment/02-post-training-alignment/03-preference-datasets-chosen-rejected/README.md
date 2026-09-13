---
name: rl-alignment-preference-datasets-chosen-rejected
title: 'Preference Datasets: Chosen vs. Rejected Response Pairs'
tags: [reinforcement-learning, nlp]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`02-instruction-vs-pretraining-datasets` built examples that teach a model to imitate ONE correct response per prompt. But "what's the single correct response" is often ambiguous or subjective — what's actually easy for a human to judge is COMPARISONS: "is response A better than response B?" A preference dataset captures exactly that comparison, and it's the foundation everything downstream in this track (reward modeling, PPO, DPO, GRPO) is built from.

### From theory to code

Implement `build_preference_pair` (packaging a prompt with two candidate responses), `shares_common_prompt_prefix` (a sanity check that both responses genuinely answer the same question), and `response_lengths`.

### Constraints

- `build_preference_pair(prompt_ids, chosen_ids, rejected_ids)` returns `{"prompt_len", "chosen", "rejected"}`, where `"chosen"`/`"rejected"` are each the FULL sequence `prompt_ids + <that response>`.
- `shares_common_prompt_prefix(preference_pair)` returns `True` exactly when both sequences' first `prompt_len` tokens are identical.
- `response_lengths(preference_pair)` returns `(chosen_response_length, rejected_response_length)`, computed as each full sequence's length minus `prompt_len`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Both `"chosen"` and `"rejected"` are built the SAME way: `prompt_ids` followed by the respective response — `shares_common_prompt_prefix` should hold trivially for any pair built with `build_preference_pair` itself, since they share the identical `prompt_ids` prefix by construction.

</details>

<details>
<summary>Hint 2</summary>

`response_lengths` doesn't need the original `chosen_ids`/`rejected_ids` lists at all — it can derive both lengths purely from the built sequences' lengths and `prompt_len`, which is exactly what `tests.py`'s independent-oracle test checks.

</details>

## Theory

### The simple version

Imagine asking two different people to answer the exact same question, then asking a judge which answer they prefer, WITHOUT the judge ever having to explain exactly what makes one answer "correct" — just which one is better. A preference dataset is a big collection of these (question, answer A, answer B, which one's preferred) records. It's much easier and cheaper to collect at scale than having humans write out a single "gold" answer for every prompt, which is exactly why RLHF and DPO are built around comparisons rather than imitation targets.

### The formula

```text
build_preference_pair(prompt, chosen, rejected):
    chosen_sequence   = prompt + chosen
    rejected_sequence = prompt + rejected
    prompt_len        = len(prompt)

shares_common_prompt_prefix(pair) = (pair.chosen[:prompt_len] == pair.rejected[:prompt_len])

response_lengths(pair) = (len(pair.chosen) - prompt_len, len(pair.rejected) - prompt_len)
```

The prompt-prefix check isn't just a formality — it's the property that makes a preference COMPARISON meaningful at all: `04-reward-modeling-bradley-terry`'s Bradley-Terry loss, `07-dpo-direct-preference-optimization`'s DPO loss, and every RLHF-family technique in this track implicitly assume both responses are answers to the exact same question.

### How PyTorch actually implements this

Context only, untested by your submission: this is exactly the structure of real preference datasets like Anthropic's HH-RLHF or OpenAI's summarization-comparison dataset used in the original InstructGPT paper (Ouyang et al., 2022) — each record is a `(prompt, chosen, rejected)` triple, collected from human annotators comparing two model outputs for the same prompt, forming the training data for `04-reward-modeling-bradley-terry`'s reward model.

## Explanation

`build_preference_pair` builds the two full sequences by prepending the SAME `prompt_ids` to each response, and records `prompt_len` so downstream code can recover exactly where the shared prefix ends and each response begins.

`shares_common_prompt_prefix` verifies the two sequences genuinely agree on their first `prompt_len` tokens — this exercise's `tests.py` confirms it correctly returns `True` for any pair built through `build_preference_pair`, and also confirms it can correctly detect `False` for a manually-constructed pair whose prompts don't actually match, proving the check does real comparison work rather than trivially always returning `True`.

`response_lengths` derives each response's length purely from the built sequences and `prompt_len` — `tests.py`'s independent-oracle test confirms this matches the response lengths computed directly from the original inputs, ruling out a version that just echoes back `len(chosen_ids)`/`len(rejected_ids)` without ever actually consulting the built pair.
