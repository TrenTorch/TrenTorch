---
title: Evaluate Expected Value in a Markov Decision Process
name: rl-expected-value-mdp
difficulty: Intermediate
tags: [rl, mdp, value-functions, fundamentals]
---

## Statement

The expected value (or expected return) of a state under a policy is the average discounted return an agent can expect to achieve starting from that state and following the policy.

### The problem, from first principles

In an MDP, the state value function V^π(s) tells you how good it is to be in state s when following policy π:

V^π(s) = E_π[G_t | S_t = s]

where G_t is the discounted return from time t onward. For a finite horizon or episodic task, you can compute this by averaging the discounted returns from many rollouts starting in state s.

### From theory to code

Implement `evaluate_state_value(trajectories, state, gamma)` which:

- Takes a list of trajectories (each is a sequence of (state, reward) tuples)
- Takes a target state s
- Takes a discount factor γ
- Returns the expected (mean) discounted return starting from the first occurrence of state s in each trajectory
- If state s does not appear in a trajectory, skip that trajectory

### Constraints

- Each trajectory is a list of (state, reward) pairs where state is hashable
- The first visit to state s is the one we care about
- Return 0.0 if the state never appears in any trajectory
- Use first-visit semantics: only the first occurrence of s in each trajectory counts

### Hints

<details>
<summary>Hint 1: Loop through trajectories</summary>
For each trajectory, find the first index where state s occurs, then compute the discounted return from that point onward.
</details>

<details>
<summary>Hint 2: Discounted return calculation</summary>
Once you identify where state s first appears, sum γ^k * reward[k+1] for all future steps.
</details>

<details>
<summary>Hint 3: Averaging</summary>
Collect all returns from state s and average them. Handle the case where s never appears.
</details>

## Theory

### The simple version

Imagine an agent runs 3 episodes. In episodes 1 and 2, state A is visited at step 1 with future rewards [5, 3]. In episode 3, state A is visited at step 0 with future rewards [7, 2]. With γ=0.9:

- Episode 1: G(A) = 5 + 0.9×3 = 7.7
- Episode 2: G(A) = 5 + 0.9×3 = 7.7
- Episode 3: G(A) = 7 + 0.9×2 = 8.8

V(A) = (7.7 + 7.7 + 8.8) / 3 = 8.07

### The formula

For each trajectory, find the first visit to state s at position i:

return_j = Σ_{k=0}^{T-i-1} γ^k · reward[i+k+1]

Then:

V^π(s) = (1/n) Σ_j return_j

where n is the number of trajectories containing s.

### Relationship to Bellman equations

The expected value satisfies:

V^π(s) = Σ_a π(a|s) Σ_{s',r} p(s',r|s,a) [r + γ·V^π(s')]

But here we estimate it from samples (Monte Carlo), not from model dynamics.

## Explanation

In practice, you can't compute V(s) directly because you don't know the environment dynamics. Instead, you collect experience (trajectories) and average the returns you see starting from s. This is called Monte Carlo evaluation. Over many trajectories, the sample average converges to the true expected value.

The first-visit constraint means: if state s appears multiple times in a single episode, only the first visit counts. This ensures samples are independent across episodes.
