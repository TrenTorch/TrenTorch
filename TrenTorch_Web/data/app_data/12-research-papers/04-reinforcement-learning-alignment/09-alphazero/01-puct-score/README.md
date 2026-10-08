---
name: research-alphazero-puct
title: 'AlphaZero: The PUCT Score'
tags: [research-papers, reinforcement-learning, self-play, search]
difficulty: Advanced
---

## Statement

### The problem, from first principles

AlphaZero (Silver et al., 2017) guides Monte Carlo tree search with a neural network. Each candidate move gets a score that balances its measured value against the network's prior, with a bonus for moves that have not been visited much.

### From theory to code

Implement `puct_score(Q, P, N_parent, N_child, c)`, returning the value plus the exploration bonus.

### Constraints

- The bonus uses the square root of the parent's visits.

### Hints

<details>
<summary>Hint 1</summary>

Compute `c * P * sqrt(N_parent) / (1 + N_child)` and add it to `Q`.

</details>

## Theory

### The simple version

Early on the prior drives the search toward likely moves, and as a move gets visited its bonus shrinks, so the search gradually trusts measured values.

### The formula

$$a^* = \arg\max_a \Big(Q(s,a) + c_{\text{puct}}\,P(s,a)\,\frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)}\Big)$$

### How NumPy/PyTorch actually implements this

Open-source AlphaZero implementations compute the same score at each node selection step.

## Explanation

The square-root form is the one used in the paper's search, and it makes the bonus grow with how often the parent has been visited.
