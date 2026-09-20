---
name: production-synthetic-data-adversarial-variants
title: Generate Single-Perturbation Adversarial Variants
tags: [production-systems, synthetic-data, evaluation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Testing whether a model is robust to small, targeted changes -- swapping one word for a synonym, replacing "ignore" with "disregard" in an injection attempt -- needs a systematic way to generate those small variants from a base example, rather than hand-writing each one.

### The task

Write `generate_adversarial_variants(base_example, perturbations)`, where `perturbations` maps a substring to find to its replacement. For each perturbation whose substring actually appears, replace its *first* occurrence and add the result to the output; skip perturbations that don't apply. `base_example` itself is never modified.

## Theory

### The simple version

Each perturbation is applied independently to a fresh copy of the base example -- one perturbation, one variant, never combined with any other perturbation in the same variant. That isolation is what makes each variant a controlled, single-variable test rather than a compounded change whose effect can't be attributed to any one substitution.

### Why skip perturbations that don't apply, rather than erroring

A single set of perturbations is often reused across many different base examples, and not every substring will exist in every example ("cat" won't appear in a sentence about cars). Silently skipping the ones that don't match lets the same perturbation set be applied broadly without every base example needing its own custom, hand-checked list.

### How this shows up in real systems

This is the mechanism behind targeted adversarial or robustness test-set generation: take a known-good example, apply one small, deliberate perturbation at a time, and check whether the model's behavior changes in a way it shouldn't -- each variant isolating exactly one substitution so a regression can be traced back to the specific change that caused it.

## Explanation

Each perturbation is checked for applicability with a plain substring test, and only applicable ones produce a variant -- `str.replace(find, replace, 1)` limits the substitution to the first occurrence, keeping every variant a single, isolated change rather than replacing every instance of the substring at once. `base_example` is a string, and strings are immutable in Python, so `.replace()` always returns a new string, leaving the original untouched by construction.
