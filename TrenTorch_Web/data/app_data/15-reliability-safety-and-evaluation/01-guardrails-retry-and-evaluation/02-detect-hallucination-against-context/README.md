---
name: agentic-guardrails-detect-hallucination
title: Detect Hallucination Against Retrieved Context
tags: [agentic-systems, guardrails, evaluation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A RAG answer is supposed to be grounded in the context it retrieved — every factual claim it makes should trace back to something the context actually said. The cheapest possible check for this doesn't need a model call at all: split the answer into individual claims, and check whether each one appears, verbatim, somewhere in the retrieved context. A claim that doesn't is flagged as unsupported — a naive but genuinely useful first-pass faithfulness check, the same kind of exact-match philosophy behind *Track Citations So Every Claim Maps to a Source*.

### From theory to code

You're given `claim_sentences` (individual sentences the answer asserted) and `context_sentences` (the retrieved context). Implement `detect_hallucination(claim_sentences, context_sentences)`. A claim is flagged as hallucinated (`True`) iff it does **not** appear verbatim (as an exact substring) within **any** context sentence. A claim appearing verbatim in at least one context sentence is grounded (`False`).

Return one bool per claim, in the same order as `claim_sentences`.

### Constraints

- 1 to 200 claims; 0 to 200 context sentences; matching is exact-substring, case-sensitive.

### Hints

<details>
<summary>Hint 1</summary>

For each claim, `any(claim in context for context in context_sentences)` checks all context sentences in one line — a claim is grounded iff that check is true for at least one of them.

</details>

<details>
<summary>Hint 2</summary>

A claim doesn't need to match a context sentence *exactly* — it just needs to appear somewhere *inside* it. `claim in context` (substring containment), not `claim == context` (exact equality), is the right check.

</details>

## Theory

### The simple version

For each claim, scan every context sentence and check whether the claim's exact text shows up inside it anywhere. If none do, the claim has no textual anchor in the retrieved context at all — flag it. This is deliberately the crudest possible check: no paraphrase detection, no semantic matching, just "does this exact string appear somewhere in what was retrieved."

### Why exact substring matching, not semantic similarity

A full faithfulness checker would use an NLI model or an LLM judge to catch paraphrased claims that are still faithful to the context's meaning — genuinely more capable, and genuinely more expensive. This naive version is worth building and understanding on its own merits: it's free (no model call), it's a real first line of defense many production systems actually run before anything fancier, and it establishes a baseline "at least this much of the answer has a literal textual anchor" that's worth having even alongside a smarter checker.

### How this shows up in real systems

Hallucination detection in production RAG systems is usually layered: a cheap substring/overlap check like this one catches the most blatant cases for free, and a more expensive NLI or LLM-judge pass (see the next question in this track) is reserved for claims that survive the cheap filter, since running the expensive check on every claim would be wasteful when a large fraction can be resolved for free.

## Explanation

For each claim, the function checks `any(claim in context for context in context_sentences)` — a claim is grounded the moment it's found as a substring of *any single* context sentence, which is why a claim spanning two separate context sentences (each containing only half of it) correctly comes back hallucinated: neither individual sentence contains the whole claim as a substring, even though the concatenated context conceptually supports it. The final list comprehension negates that check per claim (`not any(...)`), since the function's contract is "True means hallucinated," the opposite of "grounded."
