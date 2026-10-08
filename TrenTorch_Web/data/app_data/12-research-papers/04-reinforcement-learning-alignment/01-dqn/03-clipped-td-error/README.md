---
name: research-dqn-clipped-td-error
title: 'DQN: Clipping the TD Error'
tags: [research-papers, reinforcement-learning, deep-q-learning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A large TD error produces a huge gradient, which can destabilize training. DQN clips the error to a fixed range so that a single surprising transition cannot dominate an update.

### From theory to code

Implement `clipped_td_error(td, c)`, clipping each error to `[-c, c]`.

### Constraints

- Works on scalars and arrays.

### Hints

<details>
<summary>Hint 1</summary>

Use `np.clip` with bounds `-c` and `c`.

</details>

## Theory

### The simple version

Clipping keeps each update's magnitude bounded, which the paper uses as a practical way to make the squared loss behave like a Huber loss outside its quadratic region.

### The formula

$$\operatorname{clip}(\delta, -c, c) = \max(-c, \min(c, \delta))$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.smooth_l1_loss` gives the Huber version of this objective in one call.

## Explanation

Clipping the error gives the same gradient bound as the Huber loss, which is why later DQN implementations use Huber loss directly.
