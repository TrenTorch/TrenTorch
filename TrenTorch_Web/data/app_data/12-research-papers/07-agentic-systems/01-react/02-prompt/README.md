---
name: research-react-prompt
title: 'ReAct: Building the Trace Prompt'
tags: [research-papers, agents, reasoning, tool-use]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The ReAct prompt is the whole history of the episode: the question, then every thought, action and observation so far. The model conditions its next thought on that history.

### From theory to code

Implement `build_react_prompt(question, steps)`, returning the question followed by the formatted steps.

### Constraints

- Each step occupies three labelled lines.

### Hints

<details>
<summary>Hint 1</summary>

Start with the question line, then append one three-line block per step, and join with newlines.

</details>

## Theory

### The simple version

Keeping the full trace in the prompt is what lets the model use earlier observations when choosing the next action.

### The formula

$$\text{prompt}_t = [\,q,\ (\tau_1, a_1, o_1), \ldots, (\tau_{t-1}, a_{t-1}, o_{t-1})\,]$$

### How NumPy/PyTorch actually implements this

ReAct reference implementations format the scratchpad with the same Thought, Action, Observation labels.

## Explanation

The prompt grows with every step, so long episodes need trace truncation or summarization in practice.
