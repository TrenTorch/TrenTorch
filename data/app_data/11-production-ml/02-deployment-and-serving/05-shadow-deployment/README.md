---
name: production-ml-shadow-deployment
title: 'Shadow Deployment: Running a New Model Silently Alongside the Live One'
tags: [mlops]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`04-canary-deployment` exposes a slice of REAL users to a new model — which is safer than a full rollout, but still carries real risk, since canary users genuinely experience the new model's behavior. Shadow deployment removes that risk entirely: run the new model on every request too, but NEVER show its output to anyone or act on it — purely to observe how it WOULD have behaved, with zero user-facing exposure.

### From theory to code

Implement `shadow_deploy` (running both models, returning only the live one's output), `outputs_agree` (a tolerant comparison), and `compute_agreement_rate`, quantifying how often the shadow would have matched the live model.

### Constraints

- `shadow_deploy(request, live_model_fn, shadow_model_fn)` returns `{"response", "shadow_output", "shadow_error"}` — `"response"` is ALWAYS the live model's output.
- A shadow model exception must be caught and recorded in `"shadow_error"`, never allowed to affect `"response"` or propagate.
- A LIVE model exception, in contrast, must propagate normally — a broken live model is a real incident, not something to silently mask.
- `outputs_agree` compares numeric outputs within a small tolerance, everything else with exact equality.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The live model call and the shadow model call need genuinely DIFFERENT error-handling: the live one should raise like any normal function call (it's a real production incident if it fails), while the shadow one needs to be wrapped in its own `try`/`except` so a broken CANDIDATE model never takes down the real response.

</details>

<details>
<summary>Hint 2</summary>

`compute_agreement_rate` is a straightforward application of `outputs_agree` across a whole list of (live, shadow) pairs — no new comparison logic needed, just averaging the boolean results.

</details>

## Theory

### The simple version

Imagine a hospital letting a trainee doctor silently write their OWN diagnosis for every real patient, purely for evaluation — the trainee's diagnosis is compared afterward against what the attending physician actually did, but the trainee's opinion NEVER reaches the patient or affects their treatment in any way. If the trainee makes a mistake, no patient is ever harmed, since their diagnosis was never acted on — it only ever existed as a data point for evaluating the trainee's readiness. Shadow-deploying a model is exactly this: run it on real inputs, compare its answers against the real ones, but never let it touch a real outcome.

### The formula

```text
shadow_deploy(request, live_fn, shadow_fn):
    live_output = live_fn(request)                    -- let this raise normally
    try: shadow_output = shadow_fn(request); shadow_error = None
    except Exception as e: shadow_output = None; shadow_error = str(e)
    return {response: live_output, shadow_output, shadow_error}

outputs_agree(a, b) = |a - b| <= tolerance   (numeric)   or   a == b   (otherwise)

compute_agreement_rate(pairs) = fraction of pairs where outputs_agree(live, shadow)
```

The asymmetric error handling (live errors propagate, shadow errors are swallowed) is the single most important design detail here — it's the exact mechanism that makes shadow deployment genuinely SAFE to run against real, unvetted, still-being-evaluated candidate models: no matter how broken the shadow model is, it can never be the reason a real request fails.

### How PyTorch actually implements this

Context only, untested by your submission: shadow deployment (sometimes called "dark launching" or "traffic mirroring") is a standard practice for validating a new model's behavior against real production traffic distribution before ANY real users are exposed to it — real infrastructure (service meshes like Istio support traffic mirroring natively) duplicates production requests to a shadow service asynchronously, specifically so the shadow's latency and any failures never affect the real response path at all.

## Explanation

`shadow_deploy` calls the live model first, allowing its exceptions to propagate normally (this exercise's `tests.py` confirms a broken live model still raises), then separately attempts the shadow model inside its own exception boundary, recording any failure without letting it touch the real response — `tests.py`'s final oracle test runs this across many calls with deliberately mismatched live/shadow outputs, confirming the returned response is ALWAYS the live model's, never accidentally the shadow's.

`outputs_agree` handles the practical reality that model outputs are often floating-point numbers, where exact equality is too strict — `tests.py` confirms tiny floating-point differences within tolerance still count as agreement, while genuinely different values (numeric or otherwise) correctly do not.

`compute_agreement_rate` aggregates many individual comparisons into the one real, actionable signal a team watches before ever promoting a shadow model toward canary or full deployment — treating an empty comparison history as vacuously fully agreeing, since there's no evidence of disagreement yet.
