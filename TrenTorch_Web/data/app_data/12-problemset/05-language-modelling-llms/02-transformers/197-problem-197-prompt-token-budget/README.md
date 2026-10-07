---
name: problem-197-prompt-token-budget
title: 'Prompt Token Budget'
tags: [problemset, transformer-llm, prompting]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'prompting'
hint: 'max(0, context_limit - prompt_tokens)'
tools: [NumPy]
---

## Statement

Compute how many tokens are still available for generation inside a context window: `context_limit - prompt_tokens`, but never below zero.

Implement `solve(context_limit,prompt_tokens)`.

**Returns.** Return a non-negative integer.

### Examples

**Example 1**

Input:

```python
solve(10, 6)
```

Output:

```text
4
```

**Example 2**

Input:

```python
solve(10, 12)
```

Output:

```text
0
```

## Theory

### The simple version

A language model can only look at a fixed number of tokens at once, the context window. Everything it reads (the prompt) and everything it writes (the generation) must fit inside it, so the room left for the answer is the window size minus the prompt length.

### The formula

$$\text{budget}=\max(0,\;L_{\text{context}}-n_{\text{prompt}})$$

## Explanation

A prompt that already exceeds the window leaves no room, and the budget is clamped to $0$ instead of going negative (second example). In practice some tokens are also reserved for special tokens or the system prompt.
