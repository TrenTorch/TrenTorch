---
name: perplexity-from-loss-company-247
title: 'perplexity-from-loss — Microsoft case'
tags: [problemset, transformer-llm, llm-evaluation, microsoft]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'Microsoft'
hint: 'exp(mean_nll)'
---

## Statement

Microsoft-inspired language-model evaluation service reports perplexity from the average token loss. You need to convert the supplied loss into perplexity accurately so model runs can be compared on the same scale.

Convert the mean negative log-likelihood per token (natural logarithm) into perplexity: $e^{\text{loss}}$.

Implement `solve(mean_nll)`.

**Returns.** Return the perplexity as a Python float.

Convert the mean negative log-likelihood per token (natural logarithm) into perplexity: $e^{\text{loss}}$.

Implement `solve(mean_nll)`.

**Returns.** Return the perplexity as a Python float.

### Examples

**Example 1**

Input:

```python
solve(2.0)
```

Output:

```text
7.389056
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

Perplexity re-expresses the loss as an effective number of choices: a perplexity of 20 means the model is on average as unsure as if it were picking uniformly among 20 words. Lower is better, and a perfect model has perplexity 1.

### The formula

$$\text{PPL}=\exp\!\Big(-\frac1N\sum_t\ln p(w_t\mid w_{<t})\Big)=e^{\text{mean NLL}}$$

### Why it matters

- Perplexity re-expresses the loss as an effective number of choices per token, which is easier to compare between models.
- It is only comparable if the same tokeniser and logarithm base are used.

### How it works

1. Exponentiate the mean negative log-likelihood (natural log).

### Worked example

A mean loss of $2$ nats gives $e^2=7.389056$: on average the model is as unsure as choosing among about $7.4$ equally likely tokens.

## Explanation

A loss of $0$ gives perplexity $1$ (second example). Perplexity is only comparable between runs that use the same tokeniser and the same logarithm base: if the loss is in bits (base 2) it must be exponentiated with $2^{(\cdot)}$ instead.
