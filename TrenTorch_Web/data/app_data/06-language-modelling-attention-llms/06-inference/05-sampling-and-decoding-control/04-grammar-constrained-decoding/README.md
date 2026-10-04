---
name: lm-grammar-constrained-decoding
title: Grammar-Constrained Decoding
tags: [decoding, structured-output, constraints]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Applications often need the model's output to be valid JSON, a number or a fixed set of labels. Asking nicely in the prompt fails some fraction of the time, and parsing failures break the pipeline. **Constrained decoding** guarantees validity by editing the logits at every step: tokens that would take the text outside the allowed language are set to `-inf` so they can never be sampled. The allowed language is described by a small state machine. At each step you ask, for every vocabulary token, whether feeding its characters to the machine from the current state stays valid, and mask the rest.

### From theory to code

Implement `advance`, `allowed_token_ids` and `mask_logits`.

### Constraints

- The state machine is a dict `transitions` mapping `(state, char)` to the next state. A character with no entry is invalid.
- `advance(transitions, state, token)` feeds the characters of `token` one at a time and returns the final state, or `None` if any character is invalid. An empty token returns `state` unchanged.
- `allowed_token_ids(transitions, state, vocab)` returns the sorted list of ids `i` such that `advance(transitions, state, vocab[i])` is not `None` and `vocab[i]` is non-empty.
- `mask_logits(logits, allowed)` returns a copy of `logits` with `-inf` at every id not in `allowed`.

### Hints

<details>
<summary>Hint 1</summary>

Multi-character tokens are common in real vocabularies, so check every character of the token, not just the first.

</details>

<details>
<summary>Hint 2</summary>

Test with the language of non-negative integers: states `'start'`, `'digits'`, with digits allowed in both and `'0'` allowed first only as the whole number.

</details>

## Theory

### The simple version

A railway only lets a train onto a track if every junction along the whole stretch is open. Each token is a train that must travel several junctions; if any is closed it is not allowed to depart.

### The formula

$$
\tilde z_i = \begin{cases} z_i & \delta^\ast(s, v_i) \ne \bot\\ -\infty & \text{otherwise}\end{cases}
$$

where $\delta^\ast$ extends the transition function to strings. After masking, softmax assigns zero probability to every invalid token, so every sampled sequence is accepted by the machine.

### How this is done in practice

Libraries such as Outlines, llama.cpp grammars, XGrammar and the structured-output modes of hosted APIs precompute the allowed set per state to avoid scanning the whole vocabulary at each step. Masking can reduce quality if the grammar forces the model into a corner, so grammars are designed to match what the model would naturally write.

## Explanation

`advance` lifts a per-character machine to tokens. The mask keeps only tokens whose entire character sequence is valid and tests with a tiny integer grammar show multi-character tokens like `12` being allowed while `1a` is not.
