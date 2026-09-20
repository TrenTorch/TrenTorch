---
name: agentic-hitl-canvas-plan-approval
title: Human Approval or Rejection of a Proposed Plan
tags: [agentic-systems, human-in-the-loop, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Unlike a single dangerous tool call, a *plan* is a whole sequence of intended actions — reviewing it before any of them run catches problems earlier and cheaper than reviewing (or gating) each action individually after the fact. But rejection can't be a dead end: if a human rejects a plan, the right response is revising it and proposing again, not discarding the entire run.

### The task

Wire the propose-review-decide cycle so a rejected plan loops back to revision and re-proposal, rather than either executing unreviewed or giving up entirely.

## Theory

### The simple version

Propose a plan, have a human review it, and branch on their decision: approved plans go to execution, rejected plans go to revision — which then loops back into proposing the *revised* plan for another round of review. The cycle can repeat as many times as needed before something is finally approved.

### Why rejection loops back to "propose," not forward to "execute" or out to nowhere

A rejected plan isn't a finished process — it's feedback that the current plan needs to change, and the natural next step is producing a *new* proposal that addresses that feedback, then reviewing that one too. Treating rejection as a dead end (discarding the whole run) throws away everything useful the human's feedback could have informed; treating it as "execute anyway" ignores the human's decision outright — both are exactly the distractor behaviors this topology has to avoid.

### How this shows up in real systems

Plan-level approval loops are common wherever an agent proposes a multi-step course of action with real consequences — the human isn't approving each individual step, they're approving (or sending back for revision) the plan as a whole before any of its steps get a chance to run, which catches a bad overall approach before wasting effort executing part of it.

## Explanation

The cycle runs propose -> review -> (execute | revise), with `revise_plan` looping back into `propose_plan` rather than terminating or jumping straight to execution — this loop is what lets an arbitrary number of review rounds happen before a plan is finally approved, each round producing a genuinely new, revised proposal rather than resubmitting the same rejected one. Neither distractor connects to anything: executing the plan regardless of the human's decision defeats the purpose of asking at all, and discarding the whole run on a single rejection throws away a workable path (revise and try again) that the topology already provides.
