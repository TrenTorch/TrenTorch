---
name: agentic-observability-replay-until-failure
title: Replay a Run's Steps Up to the First Failure
tags: [agentic-systems, agent-observability, debugging]
difficulty: Beginner
---

## Statement

### The problem, from first principles

When a run fails partway through, debugging it means reconstructing exactly what happened before it broke -- not the whole trace forever, just the prefix that actually ran. Steps that never executed (because an earlier one already failed) aren't part of the story and shouldn't be in the replay.

### The task

Write `replay_until_failure(steps)`, where each step is `(name, succeeded)`. Return the names of every step up to and including the first failed one, then stop. If every step succeeded, return every name.

## Theory

### The simple version

Walk the recorded steps in order, collecting each name as you go. The moment you hit a step that failed, include it (it's the one that broke) and stop -- anything recorded after it either didn't run or is irrelevant to explaining the failure.

### Why "up to and including," not "up to but excluding"

The failed step itself is the most important one in the replay -- it's the thing that needs debugging. Excluding it would produce a replay that shows everything leading up to the crash except the crash.

### How this shows up in real systems

This is the same idea as replaying a request trace up to the span that errored, or reading a log file up to the line where an exception was raised -- the useful prefix is "everything that happened, including the failure," not the full log including whatever came after (which, for a stopped run, is usually just nothing).

## Explanation

A single pass appends each step's name before checking whether it succeeded, so the failing step's name is always included in the output; the loop then breaks immediately, guaranteeing nothing after the first failure is ever appended -- if no step fails, the loop simply runs to completion and every name ends up in the result.
