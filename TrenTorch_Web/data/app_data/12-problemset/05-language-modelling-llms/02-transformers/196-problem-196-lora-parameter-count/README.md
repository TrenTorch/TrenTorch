---
name: problem-196-lora-parameter-count
title: 'LoRA Parameter Count'
tags: [problemset, transformer-llm, fine-tuning-and-peft]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'fine tuning and PEFT'
hint: 'r * (in_features + out_features)'
tools: [NumPy]
---

## Statement

Count the trainable parameters of a LoRA adapter of rank `r` on a layer with `in_features` inputs and `out_features` outputs: the matrices $A\in\mathbb R^{r\times d_{in}}$ and $B\in\mathbb R^{d_{out}\times r}$ together.

Implement `solve(in_features,out_features,r)`.

**Returns.** Return an integer $r\,(d_{in}+d_{out})$.

### Examples

**Example 1**

Input:

```python
solve(10, 8, 2)
```

Output:

```text
36
```

**Example 2**

Input:

```python
solve(4096, 4096, 8)
```

Output:

```text
65536
```

## Theory

### The simple version

The appeal of LoRA is how few numbers it trains. A full update of a $d_{out}\times d_{in}$ matrix has $d_{in}d_{out}$ parameters, but the low-rank pair has only $r(d_{in}+d_{out})$, which for small $r$ is a tiny fraction.

### The count

$$|A|+|B|=r\,d_{in}+d_{out}\,r=r\,(d_{in}+d_{out})$$

### Why it matters

- LoRA's appeal is how few numbers it trains compared with the full matrix.
- The count grows linearly with the rank.

### How it works

1. $A$ has $r\cdot d_{in}$ parameters.
2. $B$ has $d_{out}\cdot r$ parameters.
3. Add them: $r(d_{in}+d_{out})$.

### Worked example

With $d_{in}=10$, $d_{out}=8$ and $r=2$: $2\cdot(10+8)=36$ parameters, against $80$ for the full matrix.

## Explanation

For a $4096\times4096$ layer and $r=8$ the adapter has $65{,}536$ parameters versus $16{,}777{,}216$ in the full matrix, about $0.4\%$. The count grows linearly with the rank, so doubling $r$ doubles the adapter size.
