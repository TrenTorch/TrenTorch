---
name: hmm-state-posteriors
title: 'HMM state posteriors with forward-backward'
tags: [classical-ml, hmm, forward-backward, smoothing, posteriors]
difficulty: Advanced
---

## Statement

### Probability of each hidden state at each time

Viterbi gives one path. Often you need the probability that the hidden state is `i` at time `t`, given the whole observed sequence. That is the smoothed posterior `gamma_t(i) = p(s_t = i | obs)`, computed with the forward-backward algorithm.

- Forward: `alpha_0(i) = pi_i B[i, o_0]`, `alpha_t(j) = (sum_i alpha_(t-1)(i) A[i, j]) B[j, o_t]`.
- Backward: `beta_(T-1)(i) = 1`, `beta_t(i) = sum_j A[i, j] B[j, o_(t+1)] beta_(t+1)(j)`.
- Posterior: `gamma_t(i)` is proportional to `alpha_t(i) beta_t(i)`, normalized over `i`.

Implement `state_posteriors(pi, A, B, obs)`. It returns a `(T, K)` array whose rows sum to 1.

### Constraints

- Inputs are validated as for a forward-algorithm HMM: stochastic rows, consistent shapes, observations in `0..M-1`.
- The observation sequence must not be empty. Otherwise raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Store every forward vector, run the backward pass from the end, and combine them row by row. Normalize each row so rounding does not accumulate.

</details>

## Theory

Forward-backward is the sum-product version of Viterbi. It computes marginals instead of a best path, so it answers questions like "how confident is the model that the machine was in the overheating state at minute 17". The smoothed posterior uses future observations as well as past ones, which is why it is more accurate than running a filter forward only. It is also the E-step of Baum-Welch, the standard way to train HMMs with unlabeled sequences.

### Where this shows up in production

Smoothed posteriors are used for confidence scores on decoded speech and gesture segments, for soft labels when training a downstream model from weak HMM output, and for changepoint-style alerts where a state's probability crosses a threshold. In genomics they score the probability that a region belongs to a feature such as a coding exon.

### Using it to make decisions

Use posteriors when a downstream decision needs a probability, such as triggering a maintenance ticket only when the failure-state posterior exceeds 0.9. Calibrate that threshold on labeled sequences. If you only need a single labeling for an audit log, Viterbi is simpler and easier to explain, so keep posteriors for decisions that must be weighed.

### Pros and cons

**Pros:** exact marginals, uses the full sequence, and gives the E-step needed for training.

**Cons:** needs the full sequence before it can answer (it is offline, not streaming), storage grows with length, and the posteriors are only as calibrated as the trained model.

## Explanation

The solution stores all forward vectors, runs the backward recursion, and multiplies the two at each time. Normalizing each row turns the products into the posterior distribution, which removes any scaling constant that would otherwise depend on the sequence.
