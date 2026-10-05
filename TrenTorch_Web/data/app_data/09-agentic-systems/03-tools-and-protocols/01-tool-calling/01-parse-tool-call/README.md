---
name: agentic-parse-tool-call
title: Tool-Call Parsing
tags: [agentic-systems, tools, parsing, function-calling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

When a model decides to use a tool it emits a **tool call**: the tool's name and its arguments, usually as JSON. Models are not parsers, so the JSON arrives wrapped in friendly prose ("Sure! I'll look that up:"), inside a markdown code fence, or with the arguments themselves encoded as a JSON _string_ (the convention of some APIs). A robust agent has to find the call in this mess. A reliable method does not trust a regular expression to match braces, it asks a real JSON decoder to try parsing at every opening brace until one parse succeeds and looks like a tool call.

### From theory to code

Implement `parse_tool_call`.

### Constraints

- `parse_tool_call(text)` returns `(name, args)`. Scan the text for `{` characters from left to right. At each one try `json.JSONDecoder().raw_decode(text, index)`; skip positions where decoding fails.
- The first decoded value that is a dict containing a string `name` and an `arguments` key is the call. If `arguments` is a string, parse it with `json.loads` into a dict; otherwise it must already be a dict.
- If no such object is found, or the arguments string is not valid JSON for a dict, raise `ValueError`.

### Hints

<details>
<summary>Hint 1</summary>

`raw_decode` returns `(object, end_index)` and raises `json.JSONDecodeError` on bad input.

</details>

<details>
<summary>Hint 2</summary>

An earlier JSON object that is not a tool call (for example an example in the prose) must be skipped, not rejected.

</details>

## Theory

### The simple version

Finding a signed form in a stack of papers: you do not parse the whole stack, you look at each page until one has the right fields.

### The formula

The method is a search over start positions $i$ with $\{\,i : \text{text}[i] = \texttt{\{}\,\}$, accepting the first $i$ for which a JSON value starts at $i$ and passes the schema check $\texttt{name} \in \text{str} \wedge \texttt{arguments} \in \text{dict} \cup \text{str}$.

### How this is done in practice

OpenAI-style APIs return `arguments` as a JSON string, Anthropic-style APIs return a parsed object, and open models emit either inside XML-like tags or fences. Constrained decoding (covered in the Language Models track) avoids the problem entirely by guaranteeing valid JSON.

## Explanation

The scan tolerates prose before and after, code fences and decoy JSON. Raising `ValueError` with no match gives the agent loop a clear signal to ask the model to retry.
