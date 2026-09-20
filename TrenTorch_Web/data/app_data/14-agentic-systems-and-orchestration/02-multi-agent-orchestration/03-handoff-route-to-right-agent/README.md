---
name: agentic-orchestration-handoff-route
title: "A Handoff Mechanism: Route to the Right Agent"
tags: [agentic-systems, multi-agent, orchestration]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A conversation doesn't always stay in one agent's wheelhouse — it might start as a general question and turn into a refund request, or a bug report. A handoff mechanism watches for that shift and moves the conversation to whichever agent is actually built to handle it, rather than making one generalist agent muddle through every topic.

### From theory to code

You're given `current_agent`, the latest `message`, and `routing_rules` — an ordered list of `(keyword, target_agent)` pairs, checked in order with case-insensitive substring matching. Implement `route_handoff(current_agent, message, routing_rules)`. Return the `target_agent` of the **first** rule whose keyword appears anywhere in `message`. If no rule matches, stay with `current_agent` (no handoff).

### Constraints

- `routing_rules` has 0 to 50 entries; keyword matching is case-insensitive, plain substring (no word-boundary requirement).

### Hints

<details>
<summary>Hint 1</summary>

Lowercase the message once, up front, and compare against each rule's lowercased keyword — this handles case-insensitivity cleanly without repeatedly re-lowercasing the same message inside the loop.

</details>

<details>
<summary>Hint 2</summary>

Return the moment the first matching rule is found — don't scan the rest of the rules once a match has already been decided. The rule order matters precisely because the first match wins.

</details>

## Theory

### The simple version

Check the rules in order; the first one whose keyword shows up anywhere in the message decides where the conversation goes next. If nothing matches, nothing changes — the current agent keeps the conversation.

### Why substring matching, not exact keyword matching

Real messages are messy — "I found a bug" and "there's a bugfix needed" both plausibly signal an engineering issue, even though the keyword doesn't appear as a standalone word in exactly the same shape every time. Plain substring matching catches this broad family of phrasings with one simple rule, at the cost of occasionally matching inside an unrelated word — an acceptable tradeoff for a cheap, first-pass routing signal, especially since rule order lets more specific or more important keywords be checked first.

### How this shows up in real systems

Keyword-triggered handoff is a common, deliberately simple first line of routing in multi-agent customer-support and assistant systems — cheap to compute, easy to extend by adding a new rule, and easy to reason about (a support engineer can read the rule list top to bottom and know exactly what routes where), which matters more in practice than catching every possible phrasing perfectly.

## Explanation

The function lowercases `message` once up front, then walks `routing_rules` in order, comparing each rule's lowercased keyword against the lowercased message with a plain `in` substring check. The moment a match is found, its `target_agent` is returned immediately — this is what makes rule order meaningful, since an earlier rule's match is returned even if a later rule would also have matched the same message. If the loop finishes without any rule matching, the function falls through to returning `current_agent` unchanged, meaning no handoff happens at all.
