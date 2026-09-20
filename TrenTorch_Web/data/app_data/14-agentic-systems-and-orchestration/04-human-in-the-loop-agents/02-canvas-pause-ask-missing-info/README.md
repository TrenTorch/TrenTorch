---
name: agentic-hitl-canvas-pause-ask-missing-info
title: Pause and Ask the User for Missing Information
tags: [agentic-systems, human-in-the-loop, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

"Book me a flight" is missing a departure city, a date, and a destination — a model can either guess (often wrong, sometimes expensively wrong) or stop and ask. Asking is almost always the right call when a genuinely required piece of information is missing and guessing has real consequences; the agent run needs to actually pause, wait for a real answer, and only then continue with that answer folded in.

### The task

Drag each step onto the canvas, then wire `Start` through every step to `End`, in the order a real pause-and-ask cycle actually happens.

## Theory

### The simple version

Detect that something required is missing, pause and surface the specific question to the user, wait for and receive their answer, then resume execution using what they said. Four real steps, in that order — no step in this chain gets skipped.

### Why "pause" has to be a real, distinct step

Detecting a gap and asking for it aren't the same moment — an agent that "asks" without actually pausing (continuing to plan or act while the question is technically pending) risks acting on a guess anyway before the answer arrives. Making pause a distinct, blocking step is what guarantees the agent genuinely waits rather than merely mentioning the question and moving on.

### How this shows up in real systems

This is one of the most common human-in-the-loop patterns in production assistants: rather than silently filling in a plausible-but-wrong default for a missing required parameter, the run explicitly stops, asks a targeted question, and only proceeds once it has a real answer — trading a small amount of latency for a large reduction in "the agent did the wrong thing confidently."

## Explanation

The chain runs detect -> pause-and-ask -> receive-input -> resume, matching the real lifecycle of asking for help mid-run: nothing can be asked before the gap is detected, nothing can be received before the question is actually asked (and the run actually paused, not just planning to ask), and execution can't meaningfully resume before an answer has arrived to resume *with*. The two distractor pieces — guessing instead of asking, and aborting without telling the user anything — are both real alternatives an agent could take, and both are exactly what this pattern is designed to avoid, which is why neither belongs anywhere in the wired chain.
