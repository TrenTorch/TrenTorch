---
name: research-react-first-finish
title: 'ReAct: Detecting the Finish Action'
tags: [research-papers, agents, reasoning, tool-use]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The ReAct loop stops when the model emits a Finish action with its answer. Detecting that point tells the runner when to return the final answer rather than call another tool.

### From theory to code

Implement `first_finish_index(actions)`, returning where the episode ended, or None.

### Constraints

- Match the action name exactly.

### Hints

<details>
<summary>Hint 1</summary>

Scan the actions in order and return the first index whose name is Finish.

</details>

## Theory

### The simple version

The loop's termination is part of the agent contract: without a Finish action the runner needs a step budget instead.

### The formula

$$\tau^* = \min\{t : a_t = \text{Finish}\}$$

### How NumPy/PyTorch actually implements this

Agent loops check the action name after each step and break on Finish.

## Explanation

The episode's answer is the argument of the Finish action at that index.
