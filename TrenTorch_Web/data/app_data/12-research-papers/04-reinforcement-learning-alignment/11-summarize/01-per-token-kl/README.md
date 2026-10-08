---
name: research-summarize-per-token-kl
title: 'Learning to Summarize: The Sequence KL'
tags: [research-papers, reinforcement-learning, alignment, rlhf, summarization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Learning to summarize from human feedback (Stiennon et al., 2020) fine-tunes a summarizer with reinforcement learning, while keeping it close to a supervised reference. The penalty is a per-sequence KL estimate: how much more likely each sampled token is under the policy than under the reference.

### From theory to code

Implement `per_token_kl(logp_policy, logp_ref)`, summing the per-token log-ratio over the sequence.

### Constraints

- The estimate is taken on sampled tokens.

### Hints

<details>
<summary>Hint 1</summary>

Subtract the reference log-probabilities from the policy log-probabilities and sum.

</details>

## Theory

### The simple version

Summing over tokens gives the sequence-level divergence. Positive values mean the policy has moved toward the sampled text, and the penalty keeps summaries from drifting too far from fluent text.

### The formula

$$\widehat{\text{KL}} = \sum_{t=1}^{T}\big(\log\pi_\theta(y_t\mid y_{<t}) - \log\pi_{\text{ref}}(y_t\mid y_{<t})\big)$$

### How NumPy/PyTorch actually implements this

RLHF trainers compute this per-token log-ratio from the two models' logits on each rollout.

## Explanation

The sum is a single-sample estimate of the sequence KL, unbiased when the tokens are sampled from the policy.
