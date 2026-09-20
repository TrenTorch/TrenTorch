---
name: production-synthetic-data-quality-filter
title: Filter Low-Quality Synthetic Examples
tags: [production-systems, synthetic-data]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Generating synthetic training data mechanically (templates, model self-generation) produces volume, but not every generated example is actually usable -- some are too short to carry any real signal, and some are degenerate model outputs like a refusal or a disclaimer that leaked into what should have been a clean training example.

### The task

Write `filter_quality(examples, min_length, banned_phrases)` that keeps only examples at least `min_length` characters long and containing none of `banned_phrases`, case-insensitively, preserving original order.

## Theory

### The simple version

Two cheap, mechanical checks catch a large share of unusable generated examples: too short to be meaningful, or containing a phrase known to signal a degenerate output (a refusal, a disclaimer, a meta-comment about being a language model).

### Why length and banned phrases, specifically

Both are checks that require no model call and no manual review to apply, which matters because synthetic data pipelines commonly generate far more raw examples than will actually be used -- a cheap automatic filter that discards the obviously bad ones before anything more expensive (a quality-scoring model, human review) touches the data saves that expense from being spent on data that was never going to be usable anyway.

### How this shows up in real systems

This is the first, cheapest stage of a real data-cleaning pipeline for synthetic or scraped data: fast, deterministic filters remove the obviously unusable examples first, before any slower or costlier quality signal (a judge model, a human rater) is applied to what's left.

## Explanation

Each example is checked against both conditions independently -- too short, or containing any banned phrase (matched case-insensitively by lowercasing both sides) -- and only survives if neither applies. The surviving examples are appended in the order they were given, since filtering shouldn't reorder anything the caller didn't ask to be reordered.
