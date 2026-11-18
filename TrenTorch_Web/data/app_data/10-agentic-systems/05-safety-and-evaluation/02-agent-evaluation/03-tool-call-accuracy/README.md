---
name: agentic-tool-call-accuracy
title: Tool-Call Accuracy
tags: [agentic-systems, evaluation, tool-use, metrics]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A strong signal of whether an agent behaved correctly is whether it made the **right tool calls**. Given a reference list of expected calls and the list the agent actually made, you can score them like retrieved items. A call counts as correct only if both the tool name **and** the arguments match exactly. **Precision** is the fraction of the agent's calls that were expected (penalizing unnecessary and wrong calls), **recall** is the fraction of expected calls the agent made (penalizing missing ones) and F1 combines them. Calls are compared as a **multiset**: making the same correct call twice when it was expected once earns credit for one of them and counts the other as extra. A second, more forgiving score looks at tool _names_ only, to separate "chose the wrong tool" from "right tool, wrong arguments".

### From theory to code

Implement `tool_call_metrics`.

### Constraints

- Each call is a pair `(name, args)` with `args` a dict. Two calls are equal iff the names are equal and the argument dicts are equal (nested values included; key order does not matter).
- `tool_call_metrics(predicted, expected)` returns a dict with the float keys `precision`, `recall`, `f1` (exact match on name and args) and `name_f1` (match on names only), all computed from **multiset** intersections.
- `precision = matches / len(predicted)` and `recall = matches / len(expected)`, with `0.0` when the denominator is zero. `f1 = 2PR / (P + R)` or `0.0` if `P + R == 0`. If both lists are empty every metric is `1.0`.

### Hints

<details>
<summary>Hint 1</summary>

Convert each call to a hashable canonical key such as `(name, json.dumps(args, sort_keys=True))` and use `collections.Counter`.

</details>

<details>
<summary>Hint 2</summary>

`Counter(a) & Counter(b)` is the multiset intersection.

</details>

## Theory

### The simple version

Marking a shopping list: items you bought that are on the list earn credit, items bought that were not wanted lower your precision, items you forgot lower your recall, and buying the same item twice earns credit once.

### The formula

$$
P = \frac{|\hat C \cap C|}{|\hat C|}, \qquad R = \frac{|\hat C \cap C|}{|C|}, \qquad F_1 = \frac{2PR}{P + R}
$$

with multiset intersection $|\hat C \cap C| = \sum_x \min(\hat c_x, c_x)$.

### How this is done in practice

The Berkeley Function-Calling Leaderboard and tau-bench use exact-match and state-based comparisons like this. Arguments such as free-text queries rarely match exactly, so real graders may compare normalized values or use an LLM judge for specific fields.

## Explanation

Canonical keys plus counters keep the logic short. The `name_f1` value decomposes errors, a diagnostic used to decide whether to improve tool descriptions or argument handling.
