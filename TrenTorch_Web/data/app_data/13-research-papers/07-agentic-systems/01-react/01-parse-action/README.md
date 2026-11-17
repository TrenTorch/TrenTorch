---
name: research-react-parse-action
title: 'ReAct: Parsing an Action'
tags: [research-papers, agents, reasoning, tool-use]
difficulty: Beginner
---

## Statement

### The problem, from first principles

ReAct (Yao et al., 2022) interleaves reasoning traces with actions. The model writes a thought, then an action such as Search[query]. The environment answers with an observation, and the loop continues until the model finishes. Parsing the action is the first step of running that loop.

### From theory to code

Implement `parse_action(text)`, extracting the action name and its argument from the model output.

### Constraints

- Return None when no action line is present.

### Hints

<details>
<summary>Hint 1</summary>

Use a regular expression for `Action: name[argument]`, and return the two captured groups.

</details>

## Theory

### The simple version

The action format is a simple, parseable contract between the model and the tool runner. A strict format makes the loop robust to extra text around the action.

### The formula

$$\text{Thought}_t \rightarrow \text{Action}_t = a_t[\text{arg}] \rightarrow \text{Observation}_t$$

### How NumPy/PyTorch actually implements this

Agent frameworks parse actions with the same kind of pattern before dispatching the call.

## Explanation

The regex stops at the first closing bracket, so the argument can contain no brackets.
