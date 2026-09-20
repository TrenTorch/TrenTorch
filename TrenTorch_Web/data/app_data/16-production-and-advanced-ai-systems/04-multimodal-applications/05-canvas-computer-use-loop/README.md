---
name: production-multimodal-canvas-computer-use-loop
title: A Screenshot -> Action -> Repeat Computer-Use Loop
tags: [production-systems, multimodal, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A computer-use agent doesn't get to see the whole screen state up front and plan a fixed sequence of clicks -- every action it takes can change what's on screen in ways it can't fully predict (a page loads, a dropdown opens, an error appears). It has to look again after every action, not just once at the start.

### The task

Wire the loop: take a screenshot, analyze it (a vision model reading the current screen), decide the next action, execute it, and go back to taking a fresh screenshot -- repeating until the model decides the task is complete.

## Theory

### The simple version

This is the ReAct loop applied to a screen instead of a text environment: observe (screenshot), reason (analyze + decide), act (execute), then observe again. Nothing about the loop assumes a fixed number of steps -- it keeps observing and acting until the model itself judges the task done.

### Why a fresh screenshot after every single action, not just periodically

Skipping the screenshot after an action means the next decision is made against a screen state that might already be stale -- the click that was supposed to open a menu might have failed, or opened something unexpected, and the agent would have no way to know. Re-observing after every action is what lets the agent catch its own mistakes and unexpected UI changes as they happen, rather than compounding an error across several blind actions.

### How this shows up in real systems

This is the actual control loop behind computer-use agents (a vision-language model driving mouse and keyboard through screenshots): screenshot, reason about what's visible, pick one action, execute it, screenshot again -- every single cycle, because the screen genuinely can change in ways the agent's plan didn't anticipate.

## Explanation

The loop always re-enters at "take a screenshot" after executing an action, and "decide next action" is the only place the loop can exit, to "task complete" -- it never exits mid-cycle and never skips straight to execution without a screenshot and fresh analysis first. Both distractors describe skipping that re-observation step, which is exactly what turns a self-correcting loop into an agent blindly executing a stale plan.
