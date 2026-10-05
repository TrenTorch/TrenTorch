---
name: research-alphazero-dirichlet-mix
title: 'AlphaZero: Mixing in Dirichlet Noise'
tags: [research-papers, reinforcement-learning, self-play, search]
difficulty: Beginner
---

## Statement

### The problem, from first principles

To keep self-play from repeating the same opening, AlphaZero mixes Dirichlet noise into the prior at the root of the search. The noise forces the search to consider moves the network would otherwise ignore.

### From theory to code

Implement `dirichlet_mix(P, noise, eps)`, blending the prior with the noise.

### Constraints

- `eps` is typically 0.25 in AlphaZero.

### Hints

<details>
<summary>Hint 1</summary>

Weight the prior by `1 - eps` and the noise by `eps`.

</details>

## Theory

### The simple version

Mixing keeps most of the network's judgement while guaranteeing that unlikely moves get some attention. The Dirichlet distribution is a natural source of noise over a probability simplex.

### The formula

$$P'(a) = (1 - \epsilon)\,P(a) + \epsilon\,\eta_a, \qquad \eta \sim \text{Dir}(\alpha)$$

### How NumPy/PyTorch actually implements this

AlphaZero-style code draws `eta` with `np.random.dirichlet` and applies this blend at the root only.

## Explanation

The result is still a probability distribution when both inputs are, because the weights sum to one.
