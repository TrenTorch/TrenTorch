---
name: production-streaming-process-event-queue
title: Process an Event Queue That Arrives Out of Order
tags: [production-systems, streaming, real-time-agents]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A real-time agent's events don't always arrive in the order they were produced -- network jitter, retries, or multiple concurrent producers (a tool result racing a token chunk) can deliver them out of sequence. Processing them in arrival order rather than in the order they actually happened can render a response with its own steps scrambled.

### The task

Write `process_event_queue(events, handlers)`. Each event is `(timestamp, event_type, payload)`. Sort by timestamp first, then for each event whose `event_type` has an entry in `handlers` (a format string with one `{}` placeholder), append `handlers[event_type].format(payload)` to the result. Skip event types with no handler.

## Theory

### The simple version

Timestamp order, not arrival order, defines the real sequence of a run's events. Sort first, then process -- otherwise a legitimately later event that happened to arrive earlier gets treated as if it came first.

### Why sorting has to happen before any formatting, not interleaved with it

If events were formatted as they arrived and only reordered afterward, any side effect of formatting (a running counter, an accumulated string) would already reflect the wrong order and can't be un-done by resorting the output list. Sorting the raw events up front, before any processing touches them, is what guarantees the entire pipeline downstream sees the true sequence.

### How this shows up in real systems

This is the same reason event-sourced systems and distributed logs sort by a logical or wall-clock timestamp before replaying events, rather than trusting delivery order -- delivery order reflects network conditions, not the order the events actually occurred in.

## Explanation

`sorted(events, key=lambda event: event[0])` fixes the true order once, up front, before any handler runs. Only after that does the function look up each event's handler by type and format its payload -- an event type with no handler is simply skipped rather than raising, since a queue can carry event types a given consumer doesn't care about.
