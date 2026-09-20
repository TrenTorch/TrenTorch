---
name: production-routing-canvas-semantic-routing-by-intent
title: Semantic Routing by Query Intent
tags: [production-systems, model-routing, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Unlike code generation or classification, a support inbox doesn't come pre-labeled with a task type -- every message is just free text, and what it's actually about (billing, a technical bug, a general question) has to be inferred from its meaning before it can be routed anywhere.

### The task

Route each message to the specialized agent that matches what it's actually asking about: a billing question to the billing agent, a bug report to technical support, and a general question to the general FAQ agent.

## Theory

### The simple version

Semantic routing classifies the intent behind a message -- not its literal keywords, but what the user is actually trying to accomplish -- and sends it to whichever specialized agent is built to handle that intent.

### Why intent, not keywords

"Why was I charged twice" and "I don't understand this line on my bill" share almost no words, but both are billing questions. Routing on surface keywords misses this; routing on the message's actual intent (typically via an embedding or a classifier trained on labeled examples) catches paraphrases the first approach would miss entirely.

### How this shows up in real systems

This is exactly how a modern customer-support system triages incoming messages before a human or an agent ever responds: classify the intent first, then hand off to whichever specialized flow -- billing, technical, general -- is equipped to actually resolve that kind of request.

## Explanation

Each message routes to the agent whose specialty matches its intent, inferred from meaning rather than surface wording. Escalating everything straight to a human defeats the purpose of having specialized agents at all, and routing everything to the general agent ignores intent entirely -- both are the failure modes semantic routing exists to avoid.
