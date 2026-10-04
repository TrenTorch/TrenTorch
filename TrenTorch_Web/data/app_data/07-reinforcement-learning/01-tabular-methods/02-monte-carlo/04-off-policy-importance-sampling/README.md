---
title: Off-Policy Monte Carlo with Importance Sampling
name: rl-offpolicy-mc-importance-sampling
difficulty: Advanced
tags: [rl, monte-carlo, off-policy, importance-sampling]
---

## Statement

Off-policy MC learns about π* while following behavior policy β by reweighting episode returns using importance sampling. The weight corrects for the mismatch between behavior and target policies.

### The problem, from first principles

You have episodes from behavior policy β (e.g., ε-greedy). You want to estimate V^π*(s) or Q^π*(s,a) for the greedy policy. Importance sampling computes W_t = ∏(π(a_i|s_i) / β(a_i|s_i)) to reweight returns.

### From theory to code

Implement `estimate_off_policy_returns(episodes, gamma)` which:
- Takes episodes (list of (state, action, reward) tuples)
- Takes gamma
- Uses π (greedy) and β (uniform over non-zero actions)
- Returns dict {(state, action): weighted_value}

Compute ordinary importance sampling weight for each return.

### Constraints

- Behavior policy β is uniform over actions seen in the episode
- Target policy π is greedy w.r.t. learned Q
- Weight is product of π/β over entire trajectory from first visit
- Zero weight paths are dropped or clipped

### Hints

<details>
<summary>Hint 1: Track π and β</summary>
For each state-action, estimate π from Q and β from episode.
</details>

<details>
<summary>Hint 2: Compute importance weight</summary>
W = product of (π(a|s) / β(a|s)) along the path.
</details>

<details>
<summary>Hint 3: Weight the return</summary>
Weighted return = W * G. Average weighted returns.
</details>

## Theory

### The simple version

You follow a random policy and collect episodes. For each (s,a) you see, reweight the return by how likely π* would take that action vs. the behavior policy.

### The formula

V^π(s) = E_β[W_t * G_t | S_t = s]

where W_t = ∏_{i=t}^{T-1} π(A_i | S_i) / β(A_i | S_i)

### Ordinary vs Weighted Importance Sampling

Ordinary: average weighted returns directly. Can have infinite variance if β is small.
Weighted: divide by sum of weights. Reduces variance at the cost of bias.

### Challenges

If β(a|s) is small but π(a|s) is large, the weight explodes. This is "off-policy extrapolation": learning about rare trajectories.

## Explanation

Off-policy learning is powerful: you can learn from any data source, even suboptimal policies. But it requires careful weighting to avoid high variance or bias.
