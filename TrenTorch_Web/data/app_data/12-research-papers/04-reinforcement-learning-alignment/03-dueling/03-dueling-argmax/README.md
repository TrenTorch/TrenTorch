---
name: research-dueling-q-argmax
title: 'Dueling Networks: The Greedy Action Is Unchanged'
tags: [research-papers, reinforcement-learning, deep-q-learning, architectures]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Because V is the same for every action in a state, adding it cannot change which action has the largest Q. The greedy choice is therefore decided by the advantages alone.

### From theory to code

Implement `dueling_argmax(V, A)`, returning the greedy action of the dueling Q-function.

### Constraints

- Ties choose the lowest index.

### Hints

<details>
<summary>Hint 1</summary>

Build the dueling Q-values, then take `argmax`.

</details>

## Theory

### The simple version

The architecture separates the question 'how good is this state' from 'which action is best here'. Only the second question affects the greedy action.

### The formula

$$\arg\max_a Q(s, a) = \arg\max_a \big(A(s, a) - \bar A\big) = \arg\max_a A(s, a)$$

### How NumPy/PyTorch actually implements this

Dueling Q-networks are evaluated greedily with the same `argmax` call as plain DQN.

## Explanation

The mean subtraction is a constant across actions, so it also does not change the argmax.
