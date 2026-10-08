---
name: research-preference-segment-return
title: 'Human Preferences: Segment Returns'
tags: [research-papers, reinforcement-learning, alignment, reward-learning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The reward model scores whole segments of behaviour, not single steps. A segment's return is the sum of the per-step predictions, and comparisons are made between segment returns.

### From theory to code

Implement `segment_return(rewards)`, returning the sum of the predicted rewards.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Sum the array.

</details>

## Theory

### The simple version

Judging a clip as a whole matches how humans compare behaviour, and the model learns per-step rewards whose sums explain those judgements.

### The formula

$$R(\sigma) = \sum_{t} \hat r(s_t, a_t)$$

### How NumPy/PyTorch actually implements this

Preference datasets store segments and the reward model sums per-frame predictions in the same way.

## Explanation

The segment return is the quantity fed into the preference probability for each pair.
