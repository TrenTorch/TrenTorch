---
name: research-mrkl-arithmetic
title: 'MRKL: An Arithmetic Expert'
tags: [research-papers, agents, tool-use, modular]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

MRKL's arithmetic expert exists because language models are unreliable at exact arithmetic. Sending a simple expression to a deterministic module gives an exact answer the language model can then report.

### From theory to code

Implement `arithmetic_expert(expr)`, evaluating a simple binary expression with +, - or *.

### Constraints

- Return None for anything outside the supported form.

### Hints

<details>
<summary>Hint 1</summary>

Match the expression with a regular expression that captures two numbers and an operator, then compute the result.

</details>

## Theory

### The simple version

Restricting the grammar keeps the expert safe and predictable. Unlike a general evaluator, it cannot run arbitrary code.

### The formula

$$\text{result} = a \;\text{op}\; b, \qquad \text{op} \in \{+, -, \times\}$$

### How NumPy/PyTorch actually implements this

Calculator tools in agent frameworks restrict the grammar in the same way instead of calling eval.

## Explanation

The regular expression is the whole grammar; anything else is rejected rather than evaluated.
