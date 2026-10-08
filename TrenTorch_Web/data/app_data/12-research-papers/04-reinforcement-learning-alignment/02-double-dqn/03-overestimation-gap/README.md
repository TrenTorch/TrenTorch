---
name: research-double-dqn-overestimation-gap
title: 'Double DQN: Measuring Overestimation'
tags: [research-papers, reinforcement-learning, deep-q-learning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The Double DQN paper measures how much the standard target overestimates. Comparing the two targets for the same transition gives a direct check on the bias the method removes.

### From theory to code

Implement `overestimation_gap(max_target_q, double_target)`, returning their difference.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Subtract the Double DQN target from the max target.

</details>

## Theory

### The simple version

On average the standard target should sit above the Double DQN target when the networks disagree. A positive average gap is the signature of the upward bias.

### The formula

$$\Delta = \max_{a'} Q_{\bar\theta}(s', a') - Q_{\bar\theta}\big(s', \arg\max_{a'} Q_\theta(s', a')\big)$$

### How NumPy/PyTorch actually implements this

Diagnostic plots in DQN experiments track this quantity to show the effect of the double estimator.

## Explanation

The gap is zero when both networks pick the same action, which is why it is nonnegative in expectation.
