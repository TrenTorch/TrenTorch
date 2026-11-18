---
name: agentic-truncate-tool-output
title: Tool Output Truncation
tags: [agentic-systems, tools, context-management, truncation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A tool can return far more text than an agent should read: a web page, a log file, a database dump. Pasting it all into the context wastes tokens, costs money and pushes out the instructions the model needs. The usual defense is to **truncate** the output to a budget. Cutting only the end loses the conclusion, and cutting only the start loses the beginning, so a good truncation keeps the **head and the tail** and marks the gap with a note saying how much was removed, so the model knows the text is incomplete and can ask for the missing part.

### From theory to code

Implement `truncate_to_budget`.

### Constraints

- Treat tokens as whitespace-separated words: `tokens = text.split()`. If `len(tokens) <= max_tokens`, return `text` **unchanged**.
- Otherwise keep `head = int(max_tokens * head_frac)` tokens from the start and `tail = max_tokens - head` tokens from the end, and join `head_tokens + [marker] + tail_tokens` with single spaces, where `marker = f'[... {omitted} tokens omitted ...]'` and `omitted = len(tokens) - max_tokens`.
- `max_tokens >= 1` and `0 <= head_frac <= 1`. If `tail` is 0 the tail part is empty (use `tokens[len(tokens):]`, not `tokens[-0:]`).

### Hints

<details>
<summary>Hint 1</summary>

`tokens[-tail:]` with `tail = 0` returns everything, so slice from `len(tokens) - tail` instead.

</details>

<details>
<summary>Hint 2</summary>

The marker is not counted against the budget.

</details>

## Theory

### The simple version

Summarizing a long email by showing its opening and its closing lines with "[... 400 words omitted ...]" in between: enough to know what it is about and how it ended, and a clear sign something is missing.

### The formula

$$
\text{out} = t_{1:h} \;\|\; \texttt{[... } n - B \texttt{ tokens omitted ...]} \;\|\; t_{n-(B-h)+1:n}, \qquad h = \lfloor B\,\rho \rfloor
$$

### How this is done in practice

Coding agents truncate command output and file reads this way (keeping head and tail of logs, where the command and the error usually are). Production systems count real tokenizer tokens instead of words and often let the model request a specific range afterwards.

## Explanation

Slicing arithmetic and one careful edge case. The omitted count in the marker is what turns silent loss into information.
