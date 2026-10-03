---
name: hmm-viterbi-path
title: 'Viterbi decoding for the most likely hidden path'
tags: [classical-ml, hmm, viterbi, decoding, dynamic-programming]
difficulty: Intermediate
---

## Statement

### Find the single most likely state sequence

Given an HMM with initial probabilities `pi`, transitions `A`, and emissions `B`, the Viterbi algorithm finds the state path that maximizes `p(path, obs)`. It also returns that joint probability.

The recursion keeps, for each time `t` and state `j`, the best probability `delta_t(j)` of any path ending in `j`, plus a back-pointer to the previous state that achieved it. After the last step, it backtracks from the best final state.

Implement `viterbi(pi, A, B, obs)`, which returns `(path, prob)`.

- `path` is a list of `T` state indices.
- `prob` is the joint probability `p(path, obs)` of that path, as a float.

### Constraints

- Inputs are validated like a forward-algorithm HMM: stochastic rows, consistent shapes, observations in `0..M-1`.
- The observation sequence must not be empty. Otherwise raise `ValueError`.
- Ties may be broken in any consistent way, but the returned probability must equal the maximum over all paths.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Take `delta[:, None] * A` as the candidate scores for every (previous, current) pair, then take the argmax over the previous state for each current state.

</details>

## Theory

Viterbi is dynamic programming over the max-product semiring: the same recursion as the forward algorithm with sums replaced by maxima. It runs in `O(T K^2)` and returns exactly the most probable path, not the most probable state at each time separately. Those two can differ, which is why decoding and posterior marginals are separate tools.

### Where this shows up in production

Viterbi decoding is the workhorse of speech recognition back ends, gene and CpG-island annotation in bioinformatics, and part-of-speech tagging. In production systems it turns noisy sensor sequences into discrete states, such as machine modes or user activities, that dashboards and alerts can use directly.

### Using it to make decisions

Use Viterbi when you need one coherent labeling of a whole sequence, such as a state log for an audit. Use per-time posteriors instead when you need a confidence for each step. Check decoded states against held-out labels, and inspect transitions the decoder never produces, since a model that rarely switches states can hide real changes.

### Pros and cons

**Pros:** exact MAP path, no sampling, and easy to explain because every choice is traceable through back-pointers.

**Cons:** it gives one answer without uncertainty, its quality depends on the trained parameters, and like forward probabilities it needs log-space or scaling for long sequences.

## Explanation

The solution computes the best score per state and stores the argmax of every transition. Backtracking follows those stored pointers from the best final state, which is why the returned path is globally consistent rather than a sequence of local choices.
