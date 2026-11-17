---
name: research-gorilla-name-match
title: 'Gorilla: Checking the Called API Name'
tags: [research-papers, agents, tool-use, apis]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A generated API call is only correct if it calls the API it was meant for. Checking the function name against the retrieved API is a basic correctness test for tool calls.

### From theory to code

Implement `api_name_matches(call, api)`, comparing the function name in the call with the expected API.

### Constraints

- Compare whole names, not prefixes.

### Hints

<details>
<summary>Hint 1</summary>

Take the text before the first opening parenthesis, strip spaces, and compare it with the API name.

</details>

## Theory

### The simple version

Name checks catch the most common failure: calling a different function than intended. Argument checks are a separate, stricter step.

### The formula

$$\text{match} \iff \text{name}(\text{call}) = \text{api}$$

### How NumPy/PyTorch actually implements this

Tool-call validators in agent frameworks perform this name check before executing a call.

## Explanation

The split is on the first parenthesis, so arguments containing parentheses do not affect the name.
