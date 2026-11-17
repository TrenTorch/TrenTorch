---
name: research-cot-answers-match
title: 'Chain of Thought: Matching Numeric Answers'
tags: [research-papers, agents, reasoning, prompting]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Chain-of-thought accuracy is measured by comparing the extracted answer with the gold answer. Numbers should match by value, so that '1,000' and '1000' count as the same answer.

### From theory to code

Implement `answers_match(pred, gold)`, a tolerant comparison of two answer strings.

### Constraints

- Return a bool.

### Hints

<details>
<summary>Hint 1</summary>

Normalize by removing commas and case; compare as floats if both parse, otherwise compare the strings.

</details>

## Theory

### The simple version

Strict string matching would penalize harmless formatting differences, which would understate the reasoning ability of the model.

### The formula

$$\text{match}(p, g) = \mathbb{1}\big[\,|\operatorname{num}(p) - \operatorname{num}(g)| < \epsilon\,\big] \lor \mathbb{1}[\operatorname{norm}(p) = \operatorname{norm}(g)]$$

### How NumPy/PyTorch actually implements this

GSM8K-style evaluators implement this numeric normalization before comparison.

## Explanation

The float tolerance handles numbers printed with different decimal precision.
