---
name: txf-lm-beam-search-decoding
title: 'Beam search decoding, contrasted against greedy'
tags: [transformers, nlp]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[07-greedy-decoding]`'s core weakness: choosing the single best-looking token at EVERY step independently doesn't always add up to the best OVERALL sequence. A token that looks slightly less likely right now might open the door to a MUCH more likely continuation later, a tradeoff greedy decoding can never see, since it commits irreversibly at every single step and never looks back. Beam search fixes this by keeping several candidate sequences (`beam_width`-many "beams") alive SIMULTANEOUSLY: at every step, every surviving beam gets expanded by its own top candidates, all of those expansions get pooled together, and only the globally best `beam_width` (ranked by CUMULATIVE log-probability across the whole sequence so far, not just the newest token) survive into the next round, before expanding again.

This genuinely widens the search: a sequence that looked second-best after one step, but whose continuation turns out to be excellent, gets a real chance to survive and eventually WIN, something `[07-greedy-decoding]`'s single irreversible choice could never recover from. `beam_width=1` collapses this exactly back down to greedy decoding (only one beam ever survives, and its top-1 expansion IS the argmax), giving greedy decoding a precise, mathematically clean special case of the more general algorithm.

### From theory to code

Implement `sequence_log_prob(token_ids, ...)` (the total log-probability the model assigns to an already-complete sequence, summed over every next-token prediction it makes), and `beam_search_decode(token_ids, ..., num_new_tokens, beam_width)`, maintaining `beam_width` candidate sequences and their cumulative log-probabilities across `num_new_tokens` generation steps.

### Constraints

- Scoring uses SUMMED log-probabilities (log-probabilities are additive across independent steps; raw probabilities are NOT, since multiplying many probabilities together underflows toward `0` for long sequences).
- At every step, EVERY current beam gets expanded by its own top `beam_width` candidates FIRST, and only THEN are all beams' expansions pooled together and globally re-ranked, never ranking within one beam's expansions in isolation.
- `beam_width=1` must produce EXACTLY `[07-greedy-decoding]`'s output: with only one beam ever alive, its top-1 expansion at every step is, by definition, the single highest-scoring next token, the same `argmax` greedy decoding uses.
- The final answer is the single highest CUMULATIVE-log-probability sequence among the surviving beams after all `num_new_tokens` steps.

### Hints

<details>
<summary>Hint 1: Log-probabilities, not raw probabilities</summary>

`log_probs = logits - max(logits) - log(sum(exp(logits - max(logits))))`, a numerically-stable log-softmax (compare against `[02-deep-learning-core/03-losses/02-cross-entropy]`'s own internal `_log_softmax`). Track CUMULATIVE SUMS of these, never products of raw probabilities.

</details>

<details>
<summary>Hint 2: Expanding all beams, then globally re-ranking</summary>

```python
candidates = []
for sequence, score in beams:
    log_probs = log_softmax(next_token_logits_for(sequence))
    top_indices = np.argsort(log_probs)[-beam_width:]
    for idx in top_indices:
        candidates.append((sequence + [idx], score + log_probs[idx]))
candidates.sort(key=lambda c: c[1], reverse=True)
beams = candidates[:beam_width]
```

Every beam contributes UP TO `beam_width` candidates, so with `beam_width` beams there can be up to `beam_width^2` total candidates pooled together before the final `[:beam_width]` cut.

</details>

<details>
<summary>Hint 3: Verifying beam_width=1 matches greedy</summary>

With `beam_width=1`, there is only ever ONE beam alive, and its single top-`1` expansion is, by construction, `argmax(log_probs)` (the same index `argmax` of the RAW logits would give, since `log_softmax` is a strictly monotonic transformation of the logits), exactly `[07-greedy-decoding]`'s choice at every step.

</details>

## Theory

### The simple version

`[07-greedy-decoding]`'s writer commits to one word at a time and never reconsiders. Beam search is a small team of `beam_width` writers, each independently continuing their OWN draft, but after every single word, the team as a whole compares ALL their drafts-so-far and keeps only the `beam_width` most promising ones overall, discarding the rest, even if that means abandoning a draft that looked locally fine but is now falling behind. A draft that took a slightly less obvious word can still survive and eventually win, as long as its overall trajectory keeps outscoring the alternatives, a genuine advantage greedy's single, irrevocable writer never gets.

### The formula

```
beams = [(initial_sequence, 0.0)]
for step in range(num_new_tokens):
    candidates = []
    for sequence, score in beams:
        log_probs = log_softmax(next_token_logits(sequence))
        for token, log_prob in top_k(log_probs, beam_width):
            candidates.append((sequence + [token], score + log_prob))
    beams = top_k(candidates, beam_width, key=score)
return argmax(beams, key=score)
```

### How PyTorch actually implements this

`model.generate(input_ids, num_beams=beam_width, do_sample=False)` in Hugging Face `transformers` implements exactly this algorithm (with additional practical refinements this question omits: length normalization, to avoid unfairly favoring shorter sequences since every additional step can only ever DECREASE cumulative log-probability; early stopping once enough beams have naturally terminated). `num_beams=1` is documented to behave identically to greedy decoding, precisely because it's the same mathematical special case this question's own `beam_width=1` test verifies directly. Real production LLM serving overwhelmingly favors `[07-greedy-decoding]` or `[08-temperature-topk-sampling]` over beam search for open-ended generation (beam search's guaranteed-higher-log-probability property doesn't necessarily correlate with genuinely BETTER or more natural-sounding text, and it's meaningfully more expensive, tracking `beam_width` full sequences instead of just one), but beam search remains standard for tasks with a single, well-defined "correct" target, like machine translation, where maximizing sequence likelihood really is the right objective.

## Explanation

`sequence_log_prob` runs `[04-full-forward-pass]`'s forward pass once on a complete sequence, and sums the log-probability the model assigned to each ACTUAL next token at every position, the total log-likelihood of that specific sequence under the model. `beam_search_decode` maintains a list of `(sequence, cumulative_score)` pairs, starting from a single beam containing only the input. At every step, EVERY current beam is expanded by its own top-`beam_width` next tokens (via the same `log_softmax` and `argsort` pattern), producing up to `beam_width^2` candidate continuations, which are pooled together and globally re-sorted by cumulative score before keeping only the top `beam_width`, discarding everything else, even candidates that came from an individually-strong beam. After `num_new_tokens` steps, the single highest-scoring surviving beam is returned. With `beam_width=1`, exactly one beam survives at every step, and its sole expansion is, by construction, the single highest-scoring next token, identical to `[07-greedy-decoding]`'s `argmax` choice at every position, which is exactly why the two produce bit-identical output in that special case.
