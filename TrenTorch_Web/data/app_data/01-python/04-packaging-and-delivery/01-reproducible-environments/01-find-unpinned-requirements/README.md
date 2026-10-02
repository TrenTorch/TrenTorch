---
name: python-find-unpinned-requirements
title: Find Unpinned Requirements
tags: [python-packaging, reproducible-environments, requirements]
difficulty: Beginner
---

## Statement

Write `find_unpinned(requirements)`, which takes the lines of a `requirements.txt` file and returns the requirements that are **not** pinned to an exact version, so a reproducibility check can fail the build before anything is installed.

## Theory

A requirement like `pandas>=2.0` means "any version of pandas at or above 2.0". Install it today and tomorrow and you can get two different environments, because a new release may appear in between. That is the opposite of reproducible. Pinning means writing the exact version with `==`:

```text
numpy==1.26.4        # pinned: one specific release
pandas>=2.0          # not pinned: a range
requests             # not pinned: anything at all
```

pip's own documentation on [secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/) states the rule used by hash-checking mode: requirements must be pinned either to a URL, a filesystem path, or using `==`. Two details trip people up:

- A wildcard such as `scipy==1.*` uses `==` but still allows many releases, so it is **not** an exact pin.
- A direct reference such as `mypkg @ https://example.com/mypkg-1.0-py3-none-any.whl` names one specific file, so it counts as pinned.

A real requirements file is also full of noise: blank lines, `# comments`, option lines such as `--require-hashes`, trailing `\` line continuations, `--hash=...` options, and environment markers after a `;` (for example `; python_version < "3.9"`). A checker has to look through all of that to the requirement itself.

## Explanation

The function normalises each line first (drop the comment, the `--hash` style options, the continuation backslash and the marker), skips lines that are empty or that are option-only lines starting with `-`, and only then decides pinned or not. Doing the cleanup before the check means one regular expression, `name[extras]==version`, is enough: the version part may not contain `*`, `,` or comparison characters, which rejects wildcards and compound ranges in a single rule. Direct references (` @ `) are accepted before the regex runs because they pin a file rather than a version. The returned text is the cleaned requirement, which is the form a human wants to read in an error message.
