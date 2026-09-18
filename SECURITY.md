# Security Policy

This repo holds two different things with two different threat models:

- **`TrenTorch_CLI/`**: an educational ML framework, a local CLI and a from-scratch NumPy-based library, not a hosted service. There's no user data, no network-facing component beyond what `pip`/`git` themselves touch, and no production deployment. Real issues here look like arbitrary code execution via a crafted input, a path-traversal bug in the CLI's file handling, a dependency with a known CVE, or a workflow misconfiguration that leaks a secret.
- **`TrenTorch_Web/`**: a hosted SvelteKit application ([trentorch.com](https://trentorch.com), Cloudflare Pages) with a real user base — GitHub/Google OAuth and magic-link sign-in via Supabase, and per-user data (progress, solved questions, profile) protected by Row Level Security policies. Real issues here look like an RLS policy that's too permissive, an auth flow that leaks a token, a Supabase function callable outside its intended trust boundary, or a client-side exposure of something that should stay server-side.

Either way, real security issues are worth reporting properly rather than as a public issue.

## Reporting a Vulnerability

**Please don't open a public GitHub issue for a security vulnerability.**

Instead, use GitHub's private reporting flow:

1. Go to the [Security tab](https://github.com/TrenTorch/TrenTorch/security)
2. Click **"Report a vulnerability"**
3. Describe the issue: what's affected, how to reproduce it, and its impact

This opens a private advisory only the maintainer (and anyone you add) can see, so the issue isn't public until there's a fix.

## What's in scope

- The `tren` CLI and everything under `TrenTorch_CLI/platforms/cli/`
- The `trentorch` package generated from the curriculum (`TrenTorch_CLI/data/src/` → `TrenTorch_CLI/data/trentorch/`)
- The TrenTorch-Web app (`TrenTorch_Web/platform/`, `TrenTorch_Web/processes/`) and how it talks to Supabase
- Supabase schema, RLS policies, and function grants (`TrenTorch_Web/supabase/migrations/`)
- Authentication and session handling on TrenTorch-Web (OAuth, magic link, cookies/tokens)
- This repository's own GitHub Actions workflows (`.github/workflows/`) and their permissions/secrets handling

## What's out of scope

- The educational curriculum content itself being *pedagogically* naive or slow on purpose (e.g. the deliberately naive nested-loop `Conv2d` implementation) — that's the point of the course, not a bug
- Issues in `TrenTorch_CLI/` that only reproduce by running arbitrary untrusted code you've written yourself inside a module (this is a learn-by-building framework; a student's own in-progress local code isn't a trust boundary)
- Student code executed inside TrenTorch-Web's browser-side Pyodide sandbox — that's a designed, client-side trust boundary (a student's own in-progress code is never privileged and never touches the server), not report-worthy on its own unless it demonstrates an actual sandbox escape

## Response

This is a solo/small-team-maintained project, not a company with a security team or an SLA. Reports will be acknowledged and looked at as soon as reasonably possible, but there's no guaranteed response time.

## Supported versions

There's no formal release/versioning cadence — security fixes land on `dev`/`main`, whichever is the actual deployed/installed version for the affected component.
