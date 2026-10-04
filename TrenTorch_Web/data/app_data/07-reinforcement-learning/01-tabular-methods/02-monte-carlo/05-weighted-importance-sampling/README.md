---
title: Weighted Importance Sampling
name: rl-weighted-importance-sampling
difficulty: Advanced
tags: [rl, monte-carlo, off-policy, importance-weighting]
---

## Statement

Weighted Importance Sampling reduces variance of off-policy estimation by normalizing by the sum of importance weights. This trades unbiasedness for lower variance.

### The problem, from first principles

Ordinary importance sampling can have infinite variance when the behavior policy is far from the target. Weighted IS divides by the sum of weights: V(s) = Σ(W_i * G_i) / Σ(W_i), which reduces variance but adds bias.

### From theory to code

Implement `estimate_weighted_importance_sampling(episodes, gamma)` which:
- Takes episodes as list of (state, action, reward) tuples
- Computes importance weights
- Returns dict {(state, action): weighted_average_return}

Use the formula: V(s,a) = Σ(W_t * G_t) / Σ(W_t) for all visits.

### Constraints

- Zero weights are handled gracefully (skip or clip)
- Return dict of (state, action) -> value
- Gamma discount factor
- All episodes are valid sequences

### Hints

<details>
<summary>Hint 1: Accumulate weighted sums</summary>
Keep sum of weights and sum of weighted returns separately.
</details>

<details>
<summary>Hint 2: Compute importance weight</summary>
W_t = product of π(a|s) / β(a|s) along path from first visit.
</details>

<details>
<summary>Hint 3: Divide at the end</summary>
V(s,a) = (sum of weighted returns) / (sum of weights) for each (s,a).
</details>

## Theory

### The simple version

Collect episodes from a random policy. For each (s,a), compute how likely π* would be vs. the behavior policy. Weight returns by this ratio. Average weighted returns divided by average weight.

### The formula

V_WIS(s) = (Σ_t W_t * G_t) / (Σ_t W_t)

where W_t is the importance weight (product of π/β over trajectory).

### Ordinary vs Weighted

Ordinary: E[W * G] - unbiased but high variance if W is large.
Weighted: Σ(W*G) / Σ(W) - biased but lower variance.

### Convergence

Weighted IS converges to V^π almost surely as sample size grows, with lower variance than ordinary IS.

## Explanation

Weighted IS is the practical choice for off-policy learning: it avoids extreme weights and is easier to implement than other variance reduction techniques like per-decision IS.
