---
name: lm-stop-sequences-streaming
title: Stop Sequences & Streaming
tags: [decoding, streaming, stop-sequences]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

APIs let callers pass **stop sequences**: generation ends when the output contains one, and the stop text itself is not returned. Doing this on the full text is easy, but a streaming server must decide, token by token, which characters it can already send to the client. If the buffer ends with `"\n\nUs"` and the stop sequence is `"\n\nUser:"`, those last characters might turn out to be the start of the stop sequence, so they must be held back until the next token resolves the ambiguity. This question builds both pieces: truncating at the earliest stop, and computing how much of the buffer is safe to emit.

### From theory to code

Implement `truncate_at_stop` and `safe_emit_length`.

### Constraints

- `truncate_at_stop(text, stops)` returns `(clean_text, hit)`. If any stop string occurs in `text`, cut at the **earliest** occurrence (the smallest index among all stops) and return `(text[:index], True)`. Otherwise return `(text, False)`. Empty stop strings are ignored.
- `safe_emit_length(buffer, stops)` returns how many leading characters of `buffer` can be sent now, assuming no stop sequence has fully appeared. It is `len(buffer)` minus the length of the **longest suffix of `buffer` that is a proper prefix of some stop string**. If no suffix of the buffer is a proper prefix of a stop string, nothing is held back and the full length is returned.
- A proper prefix is shorter than the whole stop string.

### Hints

<details>
<summary>Hint 1</summary>

For the safe length, try suffix lengths from the longest possible (`min(len(buffer), longest_stop - 1)`) down to 1 and stop at the first that matches a stop's prefix.

</details>

<details>
<summary>Hint 2</summary>

`text.find(stop)` returns `-1` when absent.

</details>

## Theory

### The simple version

A mail clerk stamping outgoing letters at the words "END OF MESSAGE" must hold back a letter ending in "END OF MES" until the next word shows whether the phrase completes.

### The formula

$$
\text{hold} = \max\{\, k < \ell_{\max} : \text{buffer}[-k:] = s[:k] \text{ for some stop } s \,\}, \qquad
\text{safe} = |\text{buffer}| - \text{hold}
$$

### How this is done in practice

OpenAI-style `stop` parameters, vLLM's `stop` list and Hugging Face's `StoppingCriteria` all implement this. Streaming servers must apply the hold-back logic on the decoded text because a stop sequence can span several tokens, and a token can contain half of one.

## Explanation

Truncation looks for the earliest hit across all stops. The safe length is a small suffix-prefix overlap search, the same primitive used in string matching.
