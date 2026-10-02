---
name: python-lockfile-staleness
title: Is the Lockfile Stale?
tags: [python-packaging, reproducible-environments, lockfile, uv]
difficulty: Intermediate
---

## Statement

Write `stale_packages(declared, locked)`, which reports which declared dependencies the lockfile no longer satisfies, the check behind a `--locked` install in CI.

## Theory

A project keeps two files. The manifest (`pyproject.toml`) records what you **asked for**, usually ranges like `pandas>=2.0`. The lockfile records what the resolver **chose**: one exact version per package. Locking decides *what*; syncing installs it.

uv's [project sync docs](https://docs.astral.sh/uv/concepts/projects/sync/) define when a lockfile is out of date: when project metadata changes, for example you add a dependency or change a constraint so that the locked version is no longer allowed. Importantly, **a new release appearing on the package index does not make a lockfile stale**; you must ask for upgrades explicitly. That is exactly what makes lockfiles reproducible.

CI usually runs with `--locked`, which raises an error if the lockfile does not match the manifest, instead of silently re-resolving. (`--frozen` skips the check and trusts the lockfile as-is.)

Here, `declared` maps a package name to its minimum allowed version (the `>=` bound) and `locked` maps a name to its exact locked version. Versions are dotted integers, and they must be compared **numerically by component**: `1.10` is newer than `1.9`, which a plain string comparison gets wrong. Also, `1.2` and `1.2.0` are the same version.

## Explanation

`_version_key` turns a version string into a tuple of ints, and drops trailing zeros so `1.2` and `1.2.0` normalise to the same key. Comparing tuples is lexicographic by component, which is precisely numeric version ordering (`(1, 10) > (1, 9)`), where comparing the raw strings would put `"1.10"` before `"1.9"`. A package is stale if it is missing from the lock or locked below its minimum. A locked version above the minimum is fine, and so is a package present in the lock but not declared (that is a transitive dependency).
