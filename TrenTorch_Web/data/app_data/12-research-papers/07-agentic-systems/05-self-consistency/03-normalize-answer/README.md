---
name: research-sc-normalize-answer
title: 'Self-Consistency: Normalizing Answers'
tags: [research-papers, agents, reasoning, sampling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Sampled answers differ in capitalization, punctuation and spacing even when they mean the same thing. Normalizing them first lets the vote count equivalent answers together.

### From theory to code

Implement `normalize_answer(s)`, returning a canonical lowercase form without punctuation.

### Constraints

- Keep only lowercase letters, digits and spaces.

### Hints

<details>
<summary>Hint 1</summary>

Lowercase and strip, remove everything except letters, digits and spaces, then collapse runs of spaces.

</details>

## Theory

### The simple version

Canonicalizing before voting avoids splitting one answer into several buckets. The function is idempotent, so normalizing twice changes nothing.

### The formula

$$\operatorname{norm}(s) = \operatorname{collapse}\big(\operatorname{strip}(\operatorname{remove}_{\neg[a\text{-}z0\text{-}9\ ]}(\operatorname{lower}(s)))\big)$$

### How NumPy/PyTorch actually implements this

Evaluation code in reasoning benchmarks uses a near-identical normalizer before comparing answers.

## Explanation

Applying the normalization before counting is what the vote's canonical buckets depend on.
