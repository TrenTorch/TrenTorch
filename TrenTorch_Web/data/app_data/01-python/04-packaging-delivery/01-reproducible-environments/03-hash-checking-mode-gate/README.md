---
name: python-hash-checking-mode-gate
title: The All-or-Nothing Hash-Checking Gate
tags: [python-packaging, reproducible-environments, hashing, validation]
difficulty: Intermediate
---

## Statement

Write `check_hash_mode(requirements)`, which models pip's hash-checking mode: if any requirement carries a hash the whole file is held to the strict rules, and the function returns every violation.

## Theory

pip's hash-checking mode is **global and all-or-nothing**. Per the [secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/) docs:

- Specifying `--hash` against *any* requirement turns the mode on for the **whole** install (the `--require-hashes` flag turns it on explicitly).
- Once on, requirements must be pinned (to `==`, a URL or a path), and hashes are required for **all** requirements, including every transitive dependency.
- On a missing hash, an unpinned requirement or a mismatch, pip errors out and installs nothing.

The reason is security: if even one dependency were allowed in without a hash, an attacker would aim at exactly that one.

So a validator does not look at a requirement in isolation. It first asks "is the mode active?" by looking at the whole list, and only then applies per-requirement rules. This pattern, a mode switched on by one element and then enforced on all, shows up in many tools and it is worth being able to express cleanly.

Each requirement here is a dict: `{"name": "numpy", "spec": "==1.26.4", "hashes": ["sha256:..."]}`.

## Explanation

The first line is the gate: `any(...)` over the whole list decides whether the mode is active, and an inactive mode returns an empty list with no per-item checks at all, mirroring how plain pip installs behave. Sorting by name makes the error list deterministic, which matters for tests and for CI logs people diff. A requirement can break both rules at once, so the two checks are independent `if`s rather than `elif`. The `*` test stops a wildcard spec from passing as an exact pin.
