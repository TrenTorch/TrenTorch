---
name: research-toolformer-insert-call
title: 'Toolformer: Inserting a Call Into Text'
tags: [research-papers, agents, tool-use, toolformer]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Toolformer does not change the language model's architecture. It inserts API annotations into the training text wherever a call would have helped predict the following words, creating a dataset of calls in context.

### From theory to code

Implement `insert_call(text, pos, call)`, splicing the call into the text at a position.

### Constraints

- `pos` is a character index in the text.

### Hints

<details>
<summary>Hint 1</summary>

Slice the text before and after `pos` and place the call between the two pieces.

</details>

## Theory

### The simple version

The insertion point is the position where the call's result would have changed the model's next-token prediction. Inserting there teaches when a call is useful.

### The formula

$$\text{text}' = \text{text}[:p] \,\|\, c \,\|\, \text{text}[p:]$$

### How NumPy/PyTorch actually implements this

Toolformer's data generation inserts candidate calls with this kind of positional splice.

## Explanation

Slicing keeps all the original characters in order; only the call is new.
