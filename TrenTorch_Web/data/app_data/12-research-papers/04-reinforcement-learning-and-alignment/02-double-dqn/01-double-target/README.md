---
name: research-double-dqn-target
title: 'Double DQN: The Decoupled Target'
tags: [research-papers, reinforcement-learning, deep-q-learning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Q-learning's max over noisy estimates is biased upward, so it overestimates values. Double DQN (van Hasselt et al., 2016) decouples the choice of action from its evaluation: the online network selects the action and the target network scores it.

### From theory to code

Implement `double_q_target(r, gamma, done, q_next_online, q_next_target)` using that decoupled rule.

### Constraints

- Ties choose the lowest action index.

### Hints

<details>
<summary>Hint 1</summary>

Find `a = argmax(q_next_online)`, then use `q_next_target[a]` in the Bellman target.

</details>

## Theory

### The simple version

If one network overrates an action, the other one usually does not, so splitting selection from evaluation removes much of the upward bias.

### The formula

$$y = r + \gamma\,(1-d)\,Q_{\bar\theta}\big(s', \arg\max_{a'} Q_\theta(s', a')\big)$$

### How NumPy/PyTorch actually implements this

Most DQN libraries expose a `double_q` flag that switches to this target.

## Explanation

The only change from DQN is which network the argmax uses, a one-line difference in the target computation.
