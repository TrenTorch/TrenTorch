---
name: agentic-pii-redaction
title: PII Redaction
tags: [agentic-systems, safety, privacy, guardrails]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Agents read and write text that may contain personal data: emails, phone numbers, government ids, payment cards. Before logging a conversation, sending it to a third-party model or storing it as memory, a privacy guardrail should **redact** these items, replacing each with a typed placeholder like `[EMAIL]` so that the text stays readable but the secret is gone. Pattern matching finds the candidates, but patterns alone produce false positives: any 16-digit number looks like a card. A **Luhn checksum**, the check built into real card numbers, filters out random digit strings.

### From theory to code

Implement `luhn_valid` and `redact_pii`.

### Constraints

- `luhn_valid(digits)` takes a string of digits and returns `True` iff the Luhn checksum is valid: from the right, double every second digit, subtract 9 from doubled values above 9, and the total must be divisible by 10. Strings with fewer than 13 or more than 19 digits are invalid.
- `redact_pii(text)` applies these replacements **in this order** and returns `(redacted_text, counts)` where `counts` maps each placeholder name (`'CARD'`, `'SSN'`, `'EMAIL'`, `'PHONE'`) to the number of replacements made (only names with at least one replacement appear).
- 1. Card: regex `\b(?:\d[ -]?){12,18}\d\b`; replace with `[CARD]` only if the digits (separators removed) pass `luhn_valid`. 2. SSN: `\b\d{3}-\d{2}-\d{4}\b` to `[SSN]`. 3. Email: `[\w.+-]+@[\w-]+\.[\w.-]+` to `[EMAIL]`. 4. Phone: `\b\d{3}[-. ]\d{3}[-. ]\d{4}\b` to `[PHONE]`.

### Hints

<details>
<summary>Hint 1</summary>

Use `re.sub` with a function to decide per match whether to replace (for the card check) and to count replacements.

</details>

<details>
<summary>Hint 2</summary>

Doing cards first prevents their digits from being mistaken for phone numbers.

</details>

## Theory

### The simple version

A court clerk blacking out names and numbers on a public document: every sensitive item replaced by a label, and a checksum to avoid blacking out harmless numbers that merely look like card numbers.

### The formula

$$
\text{Luhn}(d_1 \dots d_n):\quad \sum_{i}\big(d_{n-i} \cdot [\,i \text{ odd}\,?\,2 : 1\,]\big)_{\text{digit-sum}} \equiv 0 \pmod{10}
$$

### How this is done in practice

Microsoft Presidio, AWS Comprehend and Google DLP combine patterns, checksums, dictionaries and named-entity models. Regex-only redaction misses names and addresses, so production pipelines use a model-based detector as well.

## Explanation

Each pattern is a small, ordered step. The Luhn test is the difference between redacting real card numbers and corrupting any long number in the text, and the tests include a valid and an invalid card to show it.
