---
name: production-streaming-find-cancel-point
title: Find Where a Stream Was Cancelled
tags: [production-systems, streaming, real-time-agents]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A real-time agent can be cancelled mid-response -- a user closes the chat, navigates away, or explicitly hits stop. Whatever was received before that cancellation is still valid and worth keeping; anything after it never happened as far as the user is concerned and shouldn't be processed.

### The task

Write `find_cancel_point(events)`, where each event is `(event_type, payload)` and `event_type` is one of `"chunk"`, `"tool_call"`, `"done"`, or `"cancel"`. Return the index of the first `"cancel"` event, or `None` if the stream was never cancelled.

## Theory

### The simple version

Scan the event log for the specific `"cancel"` marker and report where it happened. Everything is a plain linear scan -- there's no ambiguity about what counts as a cancellation, only about which event in the sequence carries it.

### Why this needs its own event type, not inference from silence

A stream simply stopping (no more events) could mean it finished normally, errored out, or was cancelled -- those need different handling (finished means "show the full answer," cancelled means "show what we have and stop cleanly"). An explicit `"cancel"` event removes the ambiguity: cancellation is a fact recorded in the log, not something inferred from the absence of further events.

### How this shows up in real systems

This is the same distinction an event-sourced system makes between "no more events yet" and "an explicit termination event was recorded" -- a streaming chat UI needs to tell a user-initiated stop apart from a network drop or a completed response, and it can only do that if cancellation is its own explicit signal.

## Explanation

A single linear scan checks each event's type and returns the index the instant `"cancel"` is found -- other event types (`"chunk"`, `"tool_call"`, `"done"`) are simply skipped over, since only an explicit cancel event marks the point after which nothing further should be processed.
