---
name: agentic-context-window-trimming
title: Context Window Trimming
tags: [agentic-systems, memory, context-window, short-term-memory]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A conversation grows with every turn, but the model's context window is finite and every token costs money and latency. The simplest form of agent memory is a **sliding window**: keep the most recent messages that fit in the budget and drop the oldest. Two rules keep it from breaking things. The **system message** holds the agent's instructions and must never be dropped. And the kept messages must be a **contiguous suffix** of the history: skipping a short recent message to keep a longer older one would leave the model with a conversation that has holes in it.

### From theory to code

Implement `trim_messages`.

### Constraints

- `messages` is a list of dicts with `role` and `content`. A message's cost is `len(content.split())` tokens.
- All messages with role `'system'` are always kept. The remaining messages are considered from newest to oldest and added while the running total stays within `max_tokens` (system messages count toward the total); stop at the first message that does not fit, so the kept non-system messages form a contiguous suffix.
- Return the kept messages in their **original order**. If the system messages alone exceed `max_tokens`, raise `ValueError`.
- Do not modify the input.

### Hints

<details>
<summary>Hint 1</summary>

Pay for the system messages first, then walk the other messages backwards.

</details>

<details>
<summary>Hint 2</summary>

Remember each kept message's original index to restore the order.

</details>

## Theory

### The simple version

Packing a suitcase for a short trip: the passport always goes in, then you add clothes starting from what you will need first, and stop when the case is full, you do not skip a coat and then pack socks from last week.

### The formula

$$
\text{keep} = S \cup \{m_j, m_{j+1}, \dots, m_n\}, \quad j = \min\Big\{ j : \sum_{s \in S}|s| + \sum_{i \ge j,\, i \notin S}|m_i| \le B \Big\}
$$

### How this is done in practice

Chat frameworks implement this as `trim_messages` or a conversation buffer window. The next questions in this sub-section replace deleting old messages with summarizing them, and with retrieving them only when relevant.

## Explanation

The algorithm is a budgeted backward scan. The contiguous-suffix rule is the part that is easy to violate with a greedy knapsack-style approach.
