---
name: python-parse-image-reference
title: Is This Image Reference Pinned?
tags: [python-packaging, containerization, docker, supply-chain, reproducible-environments]
difficulty: Intermediate
---

## Statement

Write `parse_image_ref(ref)`, which splits a container image reference into name, tag and digest and reports whether it is pinned to an immutable digest.

## Theory

A tag like `python:3.12` is a **mutable pointer**: the publisher can push a new image and move the tag, so the same `FROM python:3.12` builds different images on different days. A **digest** names the exact image content. Docker's [best practices](https://docs.docker.com/build/building/best-practices/) put it plainly: by pinning an image to a digest "you're guaranteed to always use the same image version, even if a publisher replaces the tag with a new image", for example:

```dockerfile
FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
```

Anatomy of a reference: `[registry[:port]/]path[:tag][@sha256:<64 hex>]`.

Parsing pitfalls:

- A colon can mean a **tag** (`python:3.12`) or a **registry port** (`localhost:5000/app`). Only a colon in the **last path segment** is a tag.
- The digest follows `@`. When a digest is present, a tag may still appear next to it and is kept for readability.
- With neither tag nor digest, Docker assumes the tag `latest`.

Reproducible builds pin the digest, then use a tool such as Dependabot (the Docker docs recommend this) to bump the pin deliberately.

## Explanation

The digest is split off first with `partition("@")`, so its `sha256:` colon can never be mistaken for a tag. Looking for a tag only in the last `/`-separated segment is what distinguishes `localhost:5000/app` (port) from `app:1.0` (tag). `latest` is only applied when there is neither a tag nor a digest, matching Docker's defaults. The `pinned` flag requires a well-formed `sha256:` plus 64 lowercase hex characters, so a truncated or typo'd digest is not treated as pinned.
