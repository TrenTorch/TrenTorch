---
name: production-streaming-handle-interrupt-input
title: Handle User Input While an Agent Is Mid-Task
tags: [production-systems, streaming, real-time-agents]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A real-time agent doesn't have the luxury of finishing one task before hearing from the user again -- messages can arrive while it's still working. Some of those messages genuinely need to interrupt what's happening ("stop, forget it"); most should just wait their turn.

### The task

Write `handle_interrupt_input(current_task, new_input, interrupt_keywords)`. If `new_input` contains any interrupt keyword (case-insensitive), return `"INTERRUPT_AND_SWITCH"` regardless of whether a task is running. Otherwise, return `"START_NEW_TASK"` if there's no current task, or `"QUEUE_AFTER_CURRENT"` if there is.

## Theory

### The simple version

Interrupt keywords always win, because they're an explicit signal the user wants the current thing stopped. Absent that signal, new input either starts fresh (nothing was running) or waits (something already is).

### Why interrupt keywords check first, unconditionally

If the interrupt check ran only while a task was active, "never mind" sent while idle would be misread as a fresh task instead of the cancellation it obviously is. Checking it first and unconditionally means the intent to interrupt is recognized whether or not there's currently anything to interrupt.

### How this shows up in real systems

This is the same decision a voice assistant or a real-time chat agent makes on every incoming message while it's still generating a response: barge-in phrases get priority handling, and everything else is queued behind whatever's already running rather than colliding with it mid-generation.

## Explanation

Interrupt keywords are checked first and unconditionally, since they represent explicit user intent that overrides whatever else is happening. Only once that's ruled out does the current task's presence decide between starting fresh and queuing -- the priority order is what keeps "never mind" from ever being misread as "start a new task" just because nothing happened to be running.
