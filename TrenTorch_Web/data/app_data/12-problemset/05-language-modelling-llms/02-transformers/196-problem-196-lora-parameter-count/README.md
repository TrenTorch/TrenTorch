---
name: problem-196-lora-parameter-count
title: 'LoRA Parameter Count'
tags: [problemset, transformer-llm, fine-tuning-and-peft]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'fine tuning and PEFT'
hint: 'r*in_features+r*out_features'
tools: [NumPy]
---

## Statement

Return trainable LoRA parameter count r * (in_features + out_features).

Signature: `def solve(in_features, out_features, r)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve(8, 6, 2)
```

Returns:

```python
28
```

### Example 2

```python
solve(1, 1, 1)
```

Returns:

```python
2
```

## Theory

The two low-rank factors contain r*in_features and out_features*r parameters.

## Explanation

Return trainable LoRA parameter count r * (in_features + out_features). The examples show concrete inputs and expected returned values.
