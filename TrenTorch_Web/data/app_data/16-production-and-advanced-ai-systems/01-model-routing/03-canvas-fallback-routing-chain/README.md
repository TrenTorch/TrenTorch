---
name: production-routing-canvas-fallback-chain
title: A Fallback Routing Chain
tags: [production-systems, model-routing, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Any single model provider can be down, rate-limited, or timing out at the exact moment a request arrives. An application that only ever calls one provider fails every request during that window, even though the same request would likely succeed against a different provider right now.

### The task

Wire a chain that tries the primary provider first, falls back to a second provider on failure, then a third on a second failure, returning the result the moment any attempt succeeds -- and only reporting total failure once every provider has been tried.

## Theory

### The simple version

A fallback chain tries providers in a fixed priority order, moving to the next one only when the current one fails, and stopping the instant one succeeds. It never retries a provider indefinitely, and it never gives up after just one failure when other providers haven't been tried yet.

### Why order matters, and why "give up on first failure" is wrong

The primary provider is usually the cheapest, fastest, or best-quality option, so it's tried first -- but a temporary blip there shouldn't sink the whole request when a perfectly good fallback exists. Returning an error immediately throws away requests that a fallback could have served; retrying the same failed provider forever wastes time on something already known to be down instead of moving on.

### How this shows up in real systems

This is the standard shape of provider failover for any external dependency an application can't fully control -- multiple LLM providers, multiple payment processors, multiple CDN edges -- try the preferred one, fall through a fixed list on failure, and only surface an error once every option has genuinely been exhausted.

## Explanation

The chain tries each provider in turn, and every attempt has two outcomes: success routes straight to returning the result, failure routes to the next provider in the priority order. Only the final fallback's failure routes to "all providers failed" -- an earlier failure never gives up early, because a later provider hasn't been tried yet. Retrying the same provider forever and returning an error immediately are the two failure modes this chain structurally avoids.
