---
name: problem-189-perplexity-from-nll
title: 'Perplexity from NLL'
tags: [problemset, transformer-llm, llm-evaluation]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'LLM evaluation'
hint: 'exp(mean_nll)'
tools: [NumPy]
---

## Statement

Compute the perplexity of a language model from its mean negative log-likelihood per token (natural log): $\exp(\text{mean NLL})$.

Implement `solve(mean_nll)`.

**Returns.** Return a float, at least 1 for non-negative NLL.

### Examples

**Example 1**

Input:

```python
solve(1.0)
```

Output:

```text
2.718282
```

**Example 2**

Input:

```python
solve(0.0)
```

Output:

```text
1.0
```

## Theory

### The simple version

Perplexity is the standard score for language models. It can be read as "how many equally likely words was the model effectively choosing between at each step?". A perplexity of 10 means it was as uncertain as picking uniformly among 10 words; lower is better.

### The formula

$$\text{PPL}=\exp\Big(-\frac1N\sum_{t}\log p(w_t\mid w_{<t})\Big)$$

### Why it matters

- Perplexity re-expresses the loss as an effective number of equally likely choices per token, which is easy to read and compare.
- A perfect model has perplexity $1$; lower is better.

### How it works

1. Exponentiate the mean negative log-likelihood (natural log).

### Worked example

A mean loss of $1$ nat gives $e^1=2.718282$: the model is as unsure as choosing among about $2.7$ equally likely tokens.

## Explanation

A perfect model has NLL $0$ and perplexity $1$ (second example). A model that guesses uniformly from a vocabulary of size $V$ has NLL $\ln V$ and perplexity $V$. The logarithm base must match the exponential: natural log with $e$, or base 2 with $2^{(\cdot)}$.
