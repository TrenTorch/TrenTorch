---
name: agentic-security-canvas-tool-permission-policy
title: A Tool-Permission Policy for an Agent
tags: [agentic-systems, agent-security, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Not every agent in a system needs the same access. A read-only research agent, a write-capable editing agent, and an admin agent that can delete data or run shell commands are three different trust levels, and each should hold exactly the permissions its job requires -- no more.

### The task

Wire each agent to the permissions it needs to do its job, and only those. A read-only agent must never gain write, delete, or shell access. A write agent must never gain delete or shell access. Granting an unused permission is just as wrong here as missing a required one -- it's the same mistake the Least-Privilege track studies directly.

## Theory

### The simple version

Least privilege: every principal gets the minimum set of permissions it needs, nothing extra "just in case." A permission an agent doesn't use is still a permission an attacker who compromises that agent gets to use.

### Why over-granting is a real failure, not just untidy

If a read-only agent is wired with write access it never calls, that access doesn't sit inert -- it's a live capability the moment the agent is manipulated (a prompt injection, a bug in its own reasoning, a compromised dependency). The blast radius of any single agent going wrong is bounded by exactly the permissions it holds, so the policy itself is a security control, not a code-quality nicety.

### How this shows up in real systems

Production agent platforms scope credentials per agent role rather than issuing one shared, maximally-permissioned service account -- the same principle behind IAM roles, least-privilege database users, and scoped API keys, just applied to agents instead of services.

## Explanation

Each agent connects only to the permission types its role requires: read-only gets read only, write gets read+write, admin gets all four. The forbidden connections mirror that boundary in the other direction -- read-only must never reach write, delete, or shell, and write must never reach delete or shell -- because a policy that only checks for missing grants can never catch an agent that was handed too much.
