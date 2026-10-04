---
name: lm-bio-tag-decoding
title: BIO Tagging & Entity Spans
tags: [nlp-tasks, token-classification, ner]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Fine-tuning a language model for **named entity recognition** attaches a classifier to every token. The labels use the **BIO scheme**: `B-X` marks the **b**eginning of an entity of type `X`, `I-X` marks a token **i**nside the same entity, and `O` marks a token outside any entity. The model outputs one tag per token, but what applications need is spans, such as `("PER", 0, 2)` for the first two tokens being a person. Decoding is a small state machine, and it must cope with the malformed sequences real models produce, such as an `I-X` tag that does not follow a `B-X`.

### From theory to code

Implement `decode_bio`.

### Constraints

- `tags` is a list of strings such as `'B-PER'`, `'I-PER'`, `'O'`. Return a list of `(type, start, end)` spans with `end` exclusive, in order.
- `B-X` always starts a new span. `I-X` extends the current span if one is open **and** has type `X`; otherwise (no open span, or a different type) it starts a new span of type `X` (lenient decoding). `O` closes any open span.
- A span that is still open at the end of the list is closed there.

### Hints

<details>
<summary>Hint 1</summary>

Keep the open span's type and start index while scanning.

</details>

<details>
<summary>Hint 2</summary>

Split each tag on the first `-` to get the prefix and the type.

</details>

## Theory

### The simple version

Highlighting names in a printed list: a new highlight starts at each beginning marker and keeps going while the continuation markers match its colour.

### The formula

A span is a maximal run $t_s, \dots, t_{e-1}$ with $t_s \in \{\text{B-}X, \text{I-}X\}$, $t_{s+1..e-1} = \text{I-}X$, and no `B-` tag inside. The decoder is a deterministic finite automaton over tags with $O(n)$ time.

### How this is done in practice

Hugging Face's `pipeline('ner', aggregation_strategy='simple')` and `seqeval` implement variants of this (strict mode rejects an `I-` without a preceding `B-`). Evaluation metrics for NER are computed on spans, not on tokens.

## Explanation

The state machine has three cases. The tests include all the malformed patterns the statement describes, as well as adjacent entities of the same type, where `B-` is what separates them.
