---
name: production-synthetic-data-eval-failures-to-training-set
title: Turn Eval Failures Into New Training Examples
tags: [production-systems, synthetic-data, self-improvement]
difficulty: Beginner
---

## Statement

### The problem, from first principles

An eval run tells you where a model currently fails, but that information is wasted if it just sits in a report. The most direct form of self-improvement is closing the loop: take exactly the cases the model got wrong, and turn them into new training examples targeting precisely those gaps.

### The task

Write `failures_to_training_examples(eval_results)`, where each result is `(input, expected_output, passed)`. Return a `{"input", "expected_output"}` dict for every result where `passed` is False, preserving order; drop every passing result entirely.

## Theory

### The simple version

A passing eval result confirms the model already handles that case -- there's nothing to learn from it that the model doesn't already demonstrate. A failing result is exactly where the model's current behavior and the correct behavior diverge, which is precisely the signal a new training example needs to carry.

### Why filter to only failures, rather than including everything

Including passing examples in the new training set doesn't move the model's behavior anywhere it isn't already -- it just adds volume without addressing any gap. Restricting the new dataset to genuine failures targets training effort at the cases that actually need to change, which is what makes this a self-_improvement_ loop rather than reinforcement of the status quo.

### How this shows up in real systems

This is the core mechanism behind iterative model improvement pipelines: run an eval suite, collect the failures, convert them into new training data (sometimes after human correction, sometimes used as-is with the expected output as the target), retrain or fine-tune, and re-run the eval to check the gap closed.

## Explanation

A single filtering pass keeps only the results where `passed` is False, and for each of those builds a training example carrying just the `input` and `expected_output` fields -- the `passed` flag itself isn't part of the training example, since it was only ever a marker used to decide which results to keep.
