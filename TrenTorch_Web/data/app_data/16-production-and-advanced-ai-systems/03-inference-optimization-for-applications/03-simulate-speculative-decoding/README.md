---
name: production-inference-simulate-speculative-decoding
title: Simulate Speculative Decoding
tags: [production-systems, inference-optimization]
difficulty: Medium
---

## Statement

### The problem, from first principles

Generating each token from a large model requires a full forward pass, and passes are sequential -- token N+1 can't start until token N is done. Speculative decoding speeds this up by having a small, fast "draft" model guess several tokens ahead, then having the large "target" model verify all of them in a single pass instead of generating them one at a time.

### The task

Write `simulate_speculative_decoding(draft_tokens, target_tokens)`. Count how many leading tokens match between the two (the draft's accepted prefix), then return `(accepted, output_tokens)` where `output_tokens` is the accepted prefix plus exactly one more token from `target_tokens` when one is available beyond what was accepted -- the target model's own correction or, if the whole draft was accepted, its next token generated normally.

## Theory

### The simple version

The draft model proposes a run of tokens cheaply. The target model checks them all at once: however many match what the target would have generated itself, keep them for free -- that's the speedup, since one target pass verified several tokens instead of generating just one. The moment a mismatch shows up, everything after it is thrown away, and the target model's own token at that position replaces the draft's wrong guess.

### Why exactly one bonus token, never zero

A single target forward pass computes a probability distribution for every position it just verified, including one position past the longest accepted prefix -- that next-token distribution is a byproduct of the same pass, essentially free to sample from. So even in the best case, where every draft token was accepted, the target model still contributes one further token before the next round of drafting begins; it's never wasted, and it's also never more than one.

### How this shows up in real systems

This is the actual algorithm behind speculative decoding as deployed in production LLM serving: draft models generate a handful of tokens per round, and the accepted-prefix-plus-one-correction pattern is exactly why average per-token latency drops even though the target model still ultimately verifies every emitted token exactly once.

## Explanation

`accepted` counts the longest matching prefix by walking both token lists together and stopping at the first divergence (or when one list runs out). The output then takes that many tokens from `target_tokens` and appends one more whenever the target has a token beyond the accepted prefix -- the mismatch's correction, or the next natural token when the draft was accepted in full -- and appends nothing further when the target itself has no more tokens to give.
