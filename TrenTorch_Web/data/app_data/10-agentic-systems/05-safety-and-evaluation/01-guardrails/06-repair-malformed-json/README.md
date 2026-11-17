---
name: agentic-repair-malformed-json
title: Malformed JSON Repair
tags: [agentic-systems, robustness, structured-output, parsing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Even when asked for JSON, models produce things strict parsers reject: the answer wrapped in a markdown code fence, a friendly sentence before it, a **trailing comma** after the last item, Python-style literals (`True`, `None`) instead of `true` and `null`. Rather than discarding the response and paying for a retry, an agent can apply a short sequence of conservative **repairs** and parse again. The repairs must be careful not to change meaning: a comma inside a string value is data, not a trailing comma. This question implements the common fixes in a safe order and gives up cleanly when the text still does not parse.

### From theory to code

Implement `repair_json`.

### Constraints

- `repair_json(text)` returns the parsed Python object, or raises `ValueError` if no repair makes it valid JSON. Apply these steps in order, parsing with `json.loads` after each attempt and returning at the first success (try the raw text first).
- 1. Strip a surrounding code fence (a line starting with three backticks, with an optional language name, and the closing fence). 2. Take the substring from the first `{` or `[` to the last matching closing `}` or `]` (the outermost span, ignoring leading and trailing prose). 3. Remove trailing commas: a comma followed only by whitespace and then `}` or `]`, **outside string literals**. 4. Replace the bare words `True`, `False` and `None` (outside string literals, whole words) with `true`, `false` and `null`.
- Steps accumulate: step 3 is applied to the output of step 2, and so on, attempting a parse after each.

### Hints

<details>
<summary>Hint 1</summary>

Implement string-aware scanning with a small state machine that tracks whether you are inside a double-quoted string (and handles backslash escapes), so steps 3 and 4 never touch string contents.

</details>

<details>
<summary>Hint 2</summary>

`json.loads` raises `json.JSONDecodeError`, a subclass of `ValueError`.

</details>

## Theory

### The simple version

Proofreading a form before submitting: remove the sticky note stuck on top, trim the scribbles outside the boxes, delete the stray comma and fix the casing, but never alter what someone actually wrote in an answer box.

### The formula

$$
\text{result} = \text{parse}\big(R_4 \circ R_3 \circ R_2 \circ R_1(\text{text})\big), \qquad R_i \text{ idempotent and meaning-preserving on valid JSON}
$$

### How this is done in practice

Libraries such as `json-repair` implement far more aggressive repairs. The more reliable alternative is constrained decoding or provider-side structured outputs, which prevent the problem, but repair remains a cheap safety net for open models and tool arguments.

## Explanation

A repair pipeline is only trustworthy if each step is conservative. The string-aware scanner is the core: the tests place commas and keywords inside strings to confirm they survive.
