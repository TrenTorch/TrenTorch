---
name: lm-special-tokens-chat-template
title: Special Tokens & Chat Templates
tags: [tokenization, chat-models, special-tokens]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A chat model is trained on one long stream of text, so the boundaries between a system message, a user turn and an assistant turn have to be _written into the text_ with reserved marker strings. These **special tokens** (such as `<|user|>` or `<|end|>`) must be recognized as single atomic tokens, never split by the ordinary tokenizer into pieces, and the exact template the model was fine-tuned with must be reproduced at inference time, or quality quietly degrades. Two small jobs make this concrete: render a list of messages into the template string, and split a rendered string so that special tokens stay whole while ordinary text is left for the normal tokenizer.

### From theory to code

Implement `render_chat` and `split_on_specials`.

### Constraints

- `messages` is a list of dicts with keys `role` and `content`. `render_chat(messages, add_generation_prompt)` renders each message as `<|{role}|>\n{content}<|end|>\n`, concatenated in order. If `add_generation_prompt` is true, append `<|assistant|>\n` so the model continues as the assistant.
- `split_on_specials(text, specials)` returns a list of pieces in order. Each occurrence of a string from `specials` is its own piece, and the text between occurrences is one piece (empty pieces are omitted). At any position prefer the **longest** special that matches.
- Concatenating the pieces must reproduce `text` exactly.

### Hints

<details>
<summary>Hint 1</summary>

Scan left to right: at each index test the specials sorted by length descending with `text.startswith(s, i)`.

</details>

<details>
<summary>Hint 2</summary>

Accumulate ordinary characters in a buffer and flush it whenever a special matches.

</details>

## Theory

### The simple version

The template is a screenplay format: speaker labels and stage directions are part of the script and must be typed exactly. Special tokens are the speaker labels, which the model has learned to treat as single indivisible symbols.

### The formula

For messages $m_1, \dots, m_n$ the prompt is $\bigoplus_i \texttt{<|}r_i\texttt{|>\textbackslash n}\, c_i\, \texttt{<|end|>\textbackslash n}$, optionally followed by the open assistant header. Longest-match splitting makes `<|end_of_text|>` win over a shorter special such as `<|end|>` when both could start at the same index.

### How this is done in practice

Hugging Face tokenizers ship the template as a Jinja string in `tokenizer.apply_chat_template`, and register special tokens so that they bypass the normal splitting rules. A well-known security issue follows: if user text contains a literal special-token string and the tokenizer parses it as special, the user can forge turn boundaries, so serving stacks escape or reject such strings in untrusted content.

## Explanation

The renderer is plain string assembly. The splitter is a scan with a longest-match rule, the same idea used by every tokenizer's pre-split stage, so the later byte-level or BPE encoding only ever sees the ordinary pieces.
