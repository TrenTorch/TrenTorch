---
name: agentic-hitl-canvas-apply-edits-resume
title: Apply Human Edits to a Plan and Resume Execution
tags: [agentic-systems, human-in-the-loop, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Sometimes a human doesn't want to just approve or reject a plan wholesale — they want to _change_ part of it and let the agent continue with their edits folded in. This is a step beyond simple approve/reject: the agent has to take whatever it already executed, accept the human's edits to what's left, merge those edits into the working plan, and continue — without throwing away the part that already ran, and without silently reverting to the plan as if the edits never happened.

### The task

Drag each step onto the canvas, then wire `Start` through every step to `End`, in the order a real edit-and-resume cycle actually happens.

## Theory

### The simple version

Execute up to the point where the human wants to step in, let them edit the remaining part of the plan, merge those edits into the plan the agent is actually working from, then resume execution using that merged version. Four real steps, none of them skippable.

### Why merging is a distinct step from receiving the edits

An edit a human writes exists as a standalone piece of text or structure until it's actually reconciled with the plan's current state — treating "received the edit" as the same thing as "the plan now reflects the edit" skips the part where the agent has to actually reconcile the two (the human might have edited only a subset of remaining steps, or referenced state the plan already has). Making merge an explicit step is what guarantees the plan the agent resumes with is a real, consistent combination of prior progress and the new instructions, not an ambiguous half-applied patch.

### How this shows up in real systems

Mid-execution human editing is a more collaborative variant of the simple approve/reject pattern — instead of a human only ever being able to say yes or no to a whole plan, they can redirect part of it while the agent preserves whatever legitimate progress already happened, which matters a great deal in long-running agent tasks where discarding completed work over one wanted change would be wasteful.

## Explanation

The chain runs execute-partial -> human-edits -> merge -> resume, matching the real dependency order: nothing can be edited before some part of the plan has actually run (there's no natural edit point otherwise), nothing can be merged before the edit exists, and execution can't meaningfully resume before the plan it's resuming with has actually incorporated those edits. Both distractors describe throwing away real information — discarding all progress restarts work that was already correctly completed, and resuming with the original unedited plan silently overrides what the human explicitly asked to change — which is exactly why this pattern's whole value (preserving progress _and_ respecting the edit) requires neither of them.
