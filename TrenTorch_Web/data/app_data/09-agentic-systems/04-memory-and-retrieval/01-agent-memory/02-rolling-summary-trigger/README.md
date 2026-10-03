---
name: agentic-rolling-summary-trigger
title: Rolling Summary Policy
tags: [agentic-systems, memory, summarization, context-window]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Dropping old messages loses information. A gentler policy is a **rolling summary**: when the history grows past the budget, replace the oldest messages by a short summary of them, and keep recent messages verbatim because the model needs exact recent detail. The policy question is _how many_ of the oldest messages to fold into the summary. Fold too few and you will have to summarize again next turn, fold too many and you throw away detail you could have kept. The best choice is the **smallest** number of old messages that brings the total, including the summary's own size, back under budget, never touching the most recent `keep_recent` messages.

### From theory to code

Implement `messages_to_summarize`.

### Constraints

- `token_counts` is a list with the size of each message, oldest first. `budget` is the maximum total. `summary_tokens` is the fixed size of the summary that will replace the folded messages. `keep_recent` messages at the end are protected.
- If `sum(token_counts) <= budget`, return `0` (nothing to do).
- Otherwise find the smallest `k >= 1` with `k <= len(token_counts) - keep_recent` such that `sum(token_counts[k:]) + summary_tokens <= budget` and return it. If no such `k` exists, raise `ValueError`.

### Hints

<details>
<summary>Hint 1</summary>

Folding `k` messages replaces their tokens by `summary_tokens`, so the new total is `sum(token_counts[k:]) + summary_tokens`.

</details>

<details>
<summary>Hint 2</summary>

Folding a single message is only useful if it is larger than the summary that replaces it.

</details>

## Theory

### The simple version

Tidying a desk when it overflows: you file away the oldest papers, replacing them with a one-line index card, and stop as soon as the desk is clear, always leaving today's papers where they are.

### The formula

$$
k^\ast = \min\Big\{k \ge 1 : k \le n - r,\ \sum_{i > k} t_i + s \le B\Big\} \quad\text{if } \textstyle\sum_i t_i > B,\ \text{else } 0
$$

### How this is done in practice

LangChain's summary-buffer memory and many coding agents use this pattern, with a model call to write the summary. Summaries are lossy and compound over time, so systems also keep a log of the full history outside the context to retrieve from if needed.

## Explanation

The search is a monotone scan over `k`: as `k` grows, the remaining total only shrinks. The impossible case, when even folding everything allowed does not help, must be reported rather than silently ignored.
