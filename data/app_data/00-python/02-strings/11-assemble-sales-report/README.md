---
name: python-strings-assemble-sales-report
title: "Assemble: Build a Formatted Report From Raw Text"
tags: [python-strings, formatting, parsing]
difficulty: Advanced
---

## Statement

Implement a single function that parses messy multi-line text, cleans each record, and produces an aligned report, combining slicing, immutability, trimming, splitting, case methods, formatting, and encoding.

## Theory

This problem introduces no new concepts. It combines every topic in this module the same way the "Assemble" problem in the Core Semantics module combined that module's topics. Treat the input as an immutable string: every step produces a new string, and the original is never changed.

The problem requires you to:

- Split text into lines and each line into fields (splitting).
- Remove stray whitespace from each field (trimming).
- Validate a field using a content check before converting it with `int()` or `float()` (searching and checking).
- Normalize the item label with a case method and cut it to a fixed width with a slice (case methods, slicing).
- Produce fixed-width columns and a separator line using format specifications and `*` (formatting, concatenation).
- Report a byte count for the labels (text vs bytes).

No new theory is required beyond re-reading those topics.

## Explanation

Every filter (blank/comment lines, wrong field count, non-digit quantity) is a `continue` inside one pass over `raw.splitlines()`, rather than a pre-filtering pass followed by a separate formatting pass — this keeps a skipped line from ever reaching the parts of the pipeline that assume it's valid (converting to `int`/`float`, computing a line total), and keeps every valid line's position in the output tied directly to its position in the input. The item label is title-cased *before* it's sliced to 12 characters (not the other way around), matching the spec's explicit ordering — slicing first could cut a word in half right where `.title()` would otherwise capitalize its start.
