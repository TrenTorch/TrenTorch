---
name: hmm-forward-likelihood
title: 'HMM forward algorithm for sequence likelihood'
tags: [classical-ml, hmm, sequence, forward-algorithm, likelihood]
difficulty: Intermediate
---

## Statement

### Probability of an observation sequence under an HMM

A hidden Markov model has initial probabilities `pi` (length `K`), a transition matrix `A` (`K` by `K`, row `i` gives `p(next state j | state i)`), and an emission matrix `B` (`K` by `M`, row `i` gives `p(symbol m | state i)`). Observations are integers in `0..M-1`.

The forward recursion computes `p(obs)` without enumerating state paths:

- `alpha_0(i) = pi_i * B[i, o_0]`
- `alpha_t(j) = (sum_i alpha_(t-1)(i) A[i, j]) * B[j, o_t]`
- `p(obs) = sum_i alpha_(T-1)(i)`

Implement `forward_likelihood(pi, A, B, obs)` and return `p(obs)` as a float.

### Constraints

- `pi` sums to 1. Each row of `A` and of `B` sums to 1. All entries are nonnegative.
- Each observation must be an integer in `0..M-1`. Otherwise raise `ValueError`.
- The observation sequence must not be empty.
- Shape mismatches raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Each step is a vector-matrix product followed by an elementwise multiply with one column of `B`.

</details>

## Theory

The forward algorithm turns an exponential sum over state paths into `O(T K^2)` work by reusing partial sums. It is the basis of HMM likelihood evaluation, and it is what lets you compare two HMMs on the same sequence. The raw probabilities shrink quickly with `T`, so production code runs the recursion in log space or rescales each step, a detail this question omits to keep the math visible.

### Where this shows up in production

Forward likelihoods power anomaly detection on event streams, such as flagging a device whose telemetry sequence is improbable under the fleet's normal model. They also drive speech and gesture recognition systems that choose among word models by sequence likelihood, and sequence scoring in network intrusion detection.

### Using it to make decisions

Use it to score a sequence under a model you have already trained. Compare models only on the same sequence length or on length-normalized log-likelihood, since raw probabilities favour short sequences. Set an anomaly threshold on held-out normal sequences, and recompute it whenever the model is retrained, because likelihood scales shift between model versions.

### Pros and cons

**Pros:** exact likelihood with polynomial cost, a principled score for comparing models, and a simple recursion that is easy to verify on small cases.

**Cons:** the naive form underflows on long sequences, the model must be specified or trained correctly first, and HMMs assume the Markov property, which real event streams often violate.

## Explanation

The solution validates the stochastic matrices, runs the recursion one step at a time, and sums the final vector. Checking that every row sums to one catches the most common bug in hand-built HMMs: a transition matrix whose rows were typed in as counts instead of probabilities.
