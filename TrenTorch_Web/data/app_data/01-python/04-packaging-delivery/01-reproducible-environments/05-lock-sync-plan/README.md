---
name: python-lock-sync-plan
title: Plan a Lockfile Sync
tags: [python-packaging, reproducible-environments, lockfile, uv]
difficulty: Beginner
---

## Statement

Write `sync_plan(locked, installed, exact=True)`, which decides what to install and what to remove so an environment matches its lockfile.

## Theory

Syncing makes an environment match the lockfile. The [uv docs](https://docs.astral.sh/uv/concepts/projects/sync/) describe two modes:

- **Exact** syncing removes packages that are *not* in the lockfile, so the environment matches precisely. This is the default for `uv sync`.
- **Inexact** syncing installs everything the lockfile needs but leaves extraneous packages alone. This is the default for `uv run`, where deleting something you installed by hand mid-experiment would be surprising.

Either way, a package needs installing when it is missing, or installed at a different version than the lock says (a wrong version has to be replaced, not left alone).

A plan is just data: two sorted lists of names. Computing the plan separately from executing it keeps the logic pure and trivially testable, and lets a tool print a dry run.

## Explanation

The plan is built from set-like comparisons against the lock, which is the source of truth. `installed.get(name) != version` covers both "missing" (`None`) and "wrong version" in one expression. Removal is computed only when `exact` is true, and only for names the lock does not mention. Sorting makes output stable so two runs produce identical plans.
