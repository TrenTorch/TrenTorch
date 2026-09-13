---
name: rl-alignment-constitutional-ai-critique-revise
title: 'Note: Constitutional AI, Model-Written Critiques Instead of Human Labels'
tags: [reinforcement-learning, nlp]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every technique so far in this track (`03-preference-datasets-chosen-rejected` through `10-best-of-n-sampling`) assumes a human somewhere provided the preference labels or reward scores. Constitutional AI asks: can a model improve its OWN responses, and even generate its OWN preference data, using nothing but a written set of principles ("a constitution") and the model's own ability to critique and revise, with a human never directly labeling a single response?

### From theory to code

Implement `apply_critique_revision_step` (one principle-check-and-fix cycle) and `constitutional_ai_pipeline`, chaining that step across a whole list of principles, each building on the previous step's (possibly already-revised) output.

### Constraints

- `apply_critique_revision_step(response, principle, critique_fn, revise_fn)` calls `critique_fn(response, principle)`; if it returns `None`, nothing changed (`revised=False`); otherwise, `revise_fn(response, critique)` produces the new response (`revised=True`).
- `constitutional_ai_pipeline(response, principles, critique_fn, revise_fn)` applies `apply_critique_revision_step` once per principle, IN ORDER, always operating on the CURRENT (possibly already-revised) response.
- Returns `{"final_response", "critiques_applied"}`, where `critiques_applied` contains ONLY the critiques that actually triggered a revision, in the order they were applied.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`critique_fn` returning `None` means "no problem found" — don't call `revise_fn` at all in that case, and don't add anything to `critiques_applied`.

</details>

<details>
<summary>Hint 2</summary>

`constitutional_ai_pipeline`'s loop must feed each step's OUTPUT response into the NEXT step's input — never re-check the original, unrevised response against later principles, since a genuine multi-principle revision process builds cumulatively.

</details>

## Theory

### The simple version

Imagine a writer who, before publishing an essay, reads it back against a checklist of house style rules one rule at a time: for each rule, they ask "does my CURRENT draft violate this?" — if yes, they fix that specific issue and keep going with the newly-fixed draft; if no, they move on unchanged. By the end, they've potentially revised the essay several times, once per rule that actually applied, using only their own judgment and the checklist — no editor ever had to mark up the original draft by hand. Constitutional AI applies exactly this self-editing loop to a language model's own outputs, using a written "constitution" of principles instead of a style guide.

### The formula

```text
apply_critique_revision_step(response, principle, critique_fn, revise_fn):
    critique = critique_fn(response, principle)
    if critique is None:
        return {response, revised=False, critique=None}
    return {response: revise_fn(response, critique), revised=True, critique}

constitutional_ai_pipeline(response, principles, critique_fn, revise_fn):
    current = response
    critiques_applied = []
    for principle in principles:
        step = apply_critique_revision_step(current, principle, critique_fn, revise_fn)
        current = step.response
        if step.revised:
            critiques_applied.append(step.critique)
    return {final_response: current, critiques_applied}
```

The critical design detail is that each principle's check happens against the CURRENT (cumulatively revised) response, not the original — a response that violates several principles at once gets fixed one at a time, in sequence, with each fix potentially changing whether a LATER principle's check even finds a problem.

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact two-phase structure from "Constitutional AI: Harmlessness from AI Feedback" (Bai et al., 2022) — in the paper, `critique_fn` and `revise_fn` are both calls to the SAME language model being trained, prompted to critique and then revise its own output against a written constitution, and the resulting (revised) responses are used to build preference data (`03-preference-datasets-chosen-rejected`) for further training, entirely without human-written labels for the harmful/harmless comparison itself.

## Explanation

`apply_critique_revision_step` is a single conditional: no critique means no change, any real critique triggers exactly one call to `revise_fn` — this exercise's `tests.py` confirms both branches directly.

`constitutional_ai_pipeline` threads the CURRENT response through every principle in sequence, and `tests.py` specifically verifies that a later principle's `critique_fn` call genuinely sees the ALREADY-revised response from an earlier step (not the untouched original), that `critiques_applied` records only the critiques that were actually triggered (never a `None` for a principle that found no problem, and never every principle's result unconditionally) — directly ruling out a mutant that either ignores the cumulative nature of the loop or logs every principle regardless of whether it fired.
