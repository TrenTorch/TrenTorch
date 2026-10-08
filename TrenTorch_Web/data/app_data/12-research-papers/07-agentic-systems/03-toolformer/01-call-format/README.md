---
name: research-toolformer-call-format
title: 'Toolformer: Formatting an API Call'
tags: [research-papers, agents, tool-use, toolformer]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Toolformer (Schick et al., 2023) teaches a language model to call tools by inserting API calls into its own text during training. Each annotation records the call, its arguments and the result, so the model learns when a call helps.

### From theory to code

Implement `format_api_call(name, args, result)`, returning the bracketed annotation.

### Constraints

- Use the ASCII arrow `->`.

### Hints

<details>
<summary>Hint 1</summary>

Concatenate the call with its arguments in parentheses, then the arrow and the result, inside brackets.

</details>

## Theory

### The simple version

A consistent annotation format lets the model learn the call syntax and later emit it in the same form at inference time.

### The formula

$$\text{[}\,\text{name}(\text{args}) \rightarrow \text{result}\,\text{]}$$

### How NumPy/PyTorch actually implements this

Tool-calling frameworks serialize calls in the same name-arguments-result structure.

## Explanation

The annotation includes the result so the training text stays coherent after the call.
