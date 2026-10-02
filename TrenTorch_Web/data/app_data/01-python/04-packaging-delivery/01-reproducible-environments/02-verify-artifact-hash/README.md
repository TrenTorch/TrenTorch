---
name: python-verify-artifact-hash
title: Verify an Artifact Against Allowed Hashes
tags: [python-packaging, reproducible-environments, hashing, supply-chain]
difficulty: Intermediate
---

## Statement

Write `verify_artifact(data, allowed)`, which checks the bytes of a downloaded package file against the list of hashes a lock or requirements file allows, the core check behind pip's `--require-hashes` mode.

## Theory

Pinning a version says _which release_ you want. It does not prove the file you downloaded **is** that release: a compromised mirror, or a maintainer replacing a file, would still match `==1.2.0`. Hash-checking closes that gap. Each requirement carries the expected digest of its file:

```text
FooProject == 1.2 \
    --hash=sha256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

From pip's [secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/) documentation: it is possible to give **multiple hashes** for one requirement, so that several acceptable files (for example a wheel per platform, or a wheel and an sdist) can all be allowed, and a download passes if it matches **any** of them.

The [pylock.toml specification](https://packaging.python.org/en/latest/specifications/pylock-toml/) stores the same idea as `hashes = {sha256 = "..."}` and requires at least one algorithm from `hashlib.algorithms_guaranteed`, recommending SHA-256.

Python's `hashlib` computes digests; `hmac.compare_digest` compares two digests in constant time, which is the habit to use whenever you compare secrets or integrity values.

## Explanation

Every allowed entry is parsed and validated before any comparison happens. That ordering matters: a malformed or unsupported entry in a lock file is a bug in the lock file, and it should fail loudly every time, not only on the runs where no earlier entry happened to match. Digests are lower-cased because hex is case-insensitive. `hashlib.new(algorithm, data)` keeps the function generic across sha256, sha384 and sha512 instead of hard-coding one. An empty allowed list returns `False`, since nothing is permitted.
