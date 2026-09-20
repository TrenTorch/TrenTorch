---
name: agentic-hitl-canvas-escalate-confidence
title: Escalate to a Human When Confidence Falls Below a Threshold
tags: [agentic-systems, human-in-the-loop, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Not every decision needs a human, and not every decision should skip one — the right amount of human oversight scales with how confident the agent actually is in its own answer. A rigid "always ask" policy wastes a human's time on the easy cases; a rigid "never ask" policy removes oversight exactly where it's needed most: the cases the agent itself isn't sure about.

### The task

Drag each action onto the canvas, then wire each confidence band to the one response that's actually appropriate for it.

## Theory

### The simple version

Three confidence bands, three different levels of caution: high confidence acts on its own, medium confidence acts but leaves a record for someone to check later, low confidence stops and asks a human before doing anything at all.

### Why the response scales with confidence instead of being uniform

A human reviewing every single high-confidence, routine decision is oversight that doesn't actually catch anything most of the time — it just slows everything down. A human never being asked about a genuinely uncertain decision is oversight missing from exactly the place it would matter most. Scaling the response to the actual confidence level puts human attention where it has the best chance of catching a real mistake, instead of spreading it evenly regardless of how much attention any given decision actually needs.

### How this shows up in real systems

Confidence-scaled escalation is a standard pattern in production systems that mix automation with human review — content moderation, fraud detection, and agent tool-use all commonly tier their human-review rate by a confidence or risk score, rather than treating every case identically.

## Explanation

Each confidence band maps to exactly one response matched to its actual risk level: high confidence proceeds autonomously since the agent's own signal says it's very likely correct; medium confidence still proceeds (blocking on a human here would be excessive for something the agent is reasonably sure about) but logs the decision so a human can review it after the fact if needed; low confidence escalates *before* acting, since the agent's own signal says it's genuinely unsure and a wrong action taken autonomously would be the worse outcome. Neither distractor response is proportionate to any band: aborting outright is far too extreme even for low confidence (the point is escalating for a decision, not refusing to make one at all), and responding identically regardless of confidence throws away the entire signal the confidence score was providing in the first place.
