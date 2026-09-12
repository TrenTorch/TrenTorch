---
name: inf-batch-serving-metrics-ttft-tpot-itl
title: 'Compute TTFT, TPOT, ITL, and Token Throughput'
tags: [inference, serving-metrics, ttft, throughput]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[01-latency-percentiles]` measures the SPREAD of latency across requests, but LLM serving has its own vocabulary for what happens WITHIN a single streamed response. Given the timestamps at which each token of a generated response was produced (plus the request's arrival time), compute the four standard LLM serving metrics: time-to-first-token (TTFT), time-per-output-token (TPOT), inter-token latency (ITL) per gap, and overall token throughput.

### From theory to code

```
TTFT = token_timestamps[0] - request_arrival_time
ITL_i = token_timestamps[i] - token_timestamps[i-1]     for i = 1..n-1
TPOT = mean(ITL)
throughput = n_tokens / (token_timestamps[-1] - request_arrival_time)
```

### Constraints

- TTFT is measured from `request_arrival_time`, not from the first token's own generation start.
- ITL is the list of gaps between consecutive token timestamps (length `n_tokens - 1`).
- TPOT is the mean of the ITL list (`None` if fewer than 2 tokens).
- Throughput is total tokens divided by total wall-clock time from arrival to the last token.

### Hints

<details>
<summary>Hint: TPOT excludes the first token by definition</summary>

TPOT is specifically the pace of SUBSEQUENT tokens, which is why it's `mean(ITL)`, not mean including TTFT. Guard the `n_tokens == 1` case: there are no ITLs and TPOT is undefined (return `None` rather than dividing by zero).

</details>

## Theory

### The simple version

**TTFT** measures perceived responsiveness — how long a user stares at a blank screen before anything appears; it's dominated by prefill time and queueing delay ahead of it. **TPOT** measures the steady-state generation speed once streaming has started. **ITL** is the token-by-token version of TPOT: individual gaps can spike even when the average TPOT looks fine, so serving systems track the full distribution of ITLs, not just their mean. **Throughput** blends prefill and decode time together into one aggregate efficiency number.

### The formula

```
TTFT = t[0] - arrival
ITL  = [t[i] - t[i-1] for i = 1..n-1]
TPOT = mean(ITL)
throughput = n / (t[-1] - arrival)
```

These four numbers are the vocabulary every LLM serving benchmark (and SLO) is expressed in — a system can look great on throughput while being unacceptable on TTFT if it queues requests too long before starting them.

### How PyTorch actually implements this

Pure scalar/timestamp arithmetic — no tensor computation is involved, so the same function is used regardless of which framework produced the generation timestamps.

## Explanation

TPOT computed as `mean(ITL)` and as `(t_last - t_first) / (n-1)` are algebraically the same value — a telescoping sum of consecutive differences collapses to just the two endpoints — so averaging the per-gap ITLs is both the definitionally correct metric and the cheapest way to compute the aggregate pace. This telescoping property is also why `[04-simulate-continuous-batching]`'s scheduler decisions (which can pause a request mid-generation to prioritize another) show up as SPIKES in the individual ITL values without necessarily moving the overall TPOT average much — which is exactly why production systems track full ITL distributions rather than only the mean.
