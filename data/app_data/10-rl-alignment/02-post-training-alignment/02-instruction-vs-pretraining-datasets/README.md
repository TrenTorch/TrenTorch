---
name: rl-alignment-instruction-vs-pretraining-datasets
title: 'Instruction Datasets: Prompt/Response Pairs vs. Raw Next-Token Pretraining'
tags: [reinforcement-learning, nlp]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-supervised-fine-tuning-response-loss-mask` implemented the LOSS-masking mechanics of SFT — but it took for granted that a "prompt" and "response" were already separated. This question builds the actual data structure a real instruction-tuning dataset uses, and quantifies exactly how it differs from a raw pretraining example: not just "different content", but a structurally different relationship between the tokens and the loss.

### From theory to code

Implement `build_instruction_example` (turning a prompt/response pair into one training example with its own loss mask), `build_pretraining_example` (the raw-pretraining equivalent, with no prompt/response distinction), and `fraction_of_tokens_supervised`, quantifying the difference directly.

### Constraints

- `build_instruction_example(prompt_ids, response_ids, eos_token_id)` concatenates `prompt_ids + response_ids + [eos_token_id]`, with a `loss_mask` that's `False` over the prompt and `True` over the response AND the trailing EOS token.
- `build_pretraining_example(token_ids)` returns the tokens with a `loss_mask` that's `True` everywhere.
- `fraction_of_tokens_supervised(example)` returns the mean of `example["loss_mask"]`.
- A pretraining example's supervised fraction is always exactly `1.0`; an instruction example's is always strictly less than `1.0` whenever the prompt is nonempty.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The EOS token belongs in the SUPERVISED region, not the prompt — the model needs to learn to predict "stop generating now" just as much as it needs to learn the actual response content.

</details>

<details>
<summary>Hint 2</summary>

`build_instruction_example`'s `loss_mask` is exactly `[False] * len(prompt_ids) + [True] * (len(response_ids) + 1)` — the `+1` accounts for the trailing EOS token also being supervised.

</details>

## Theory

### The simple version

Imagine two very different kinds of homework: one where a student reads a long book and is tested on predicting the NEXT WORD anywhere in it (raw pretraining — every word is fair game), versus one where a student is given a specific question and graded ONLY on the quality of their written answer, never on how well they "predicted" the question itself (instruction tuning). Both use the same underlying skill (predicting what comes next), but the instruction-tuning setup deliberately withholds credit for the part the student didn't actually have to produce.

### The formula

```text
build_pretraining_example(tokens):
    input_ids = tokens
    loss_mask = [True] * len(tokens)                        -- fraction supervised = 1.0

build_instruction_example(prompt, response, eos):
    input_ids = prompt + response + [eos]
    loss_mask = [False]*len(prompt) + [True]*(len(response)+1)   -- fraction supervised < 1.0
```

The longer the prompt relative to the response, the SMALLER the fraction of tokens that actually contribute to training — this exercise's `tests.py` confirms this directly, and it's exactly why instruction-tuning datasets with very long, detailed system prompts but short responses can end up training on surprisingly few "real" tokens per example, relative to their total length.

### How PyTorch actually implements this

Context only, untested by your submission: real instruction-tuning frameworks build precisely this `input_ids`/`loss_mask` (or `labels`, with masked positions set to `-100`) structure at dataset-preprocessing time — Hugging Face's chat-template tooling, for instance, explicitly tracks which tokens came from the "user" turn (masked) versus the "assistant" turn (supervised), which is the real-world version of the prompt/response split this exercise builds from scratch.

## Explanation

`build_instruction_example` concatenates the three pieces in order and builds a matching boolean mask — `False` for every prompt position, `True` for the response AND its trailing EOS, since a model that never learns to emit EOS would generate forever.

`build_pretraining_example` has no such structure at all: every single token is both an input the model conditions on AND a target it's trained to predict, since raw pretraining has no concept of "context I was given" versus "text I produced".

`fraction_of_tokens_supervised` makes the structural difference numerically concrete: this exercise's `tests.py` confirms a pretraining example always scores exactly `1.0`, while an instruction example's score shrinks as the prompt grows relative to the response — the same underlying next-token loss machinery, applied to a genuinely smaller, deliberately chosen subset of positions.
