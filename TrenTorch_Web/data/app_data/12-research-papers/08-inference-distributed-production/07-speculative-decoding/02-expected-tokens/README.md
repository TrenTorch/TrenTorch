---
name: research-spec-expected-tokens
title: 'Speculative Decoding: Expected Accepted Tokens'
tags: [research-papers, systems, inference, decoding]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Each speculative step yields the longest accepted prefix of the draft, plus one token from the target. If each draft token is accepted with probability alpha, the expected number of tokens per target pass is a geometric sum.

### From theory to code

Implement `expected_tokens_accepted(alpha, gamma)`, the expected tokens generated per target call.

### Constraints

- Assume the acceptance events are independent with rate alpha.

### Hints

<details>
<summary>Hint 1</summary>

Sum alpha to the power k for k from zero to gamma, which telescopes to the closed form.

</details>

## Theory

### The simple version

A high acceptance rate means each costly target pass yields several tokens, so decoding gets faster even though it runs the target model less often.

### The formula

$$\mathbb{E}[\text{tokens}] = \sum_{k=0}^{\gamma}\alpha^k = \frac{1 - \alpha^{\gamma+1}}{1 - \alpha}$$

### How NumPy/PyTorch actually implements this

Speculative decoding benchmarks compare measured tokens per pass against this expectation.

## Explanation

The closed form is the geometric series sum; the leading one is the token the target always produces.
