---
name: rl-alignment-best-of-n-sampling
title: "Best-of-N: Sampling N Responses and Picking the Reward Model's Favorite"
tags: [reinforcement-learning, nlp]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`09-rejection-sampling-finetuning` used a reward model to curate TRAINING data. Best-of-N uses the exact same "sample many, keep the best" idea, but at INFERENCE time instead: rather than changing the model's weights at all, just generate `N` candidate responses to a single prompt right now, score them with the reward model, and return only the winner to the user.

### From theory to code

Implement `best_of_n_select` (picking the single best already-sampled response) and `expected_best_of_n_reward`, a Monte-Carlo simulation quantifying how much reward best-of-`N` actually buys you as `N` grows.

### Constraints

- `best_of_n_select(responses, rewards)` returns `(best_response, best_reward)` — the response with the highest reward, and that reward.
- `expected_best_of_n_reward(reward_pool, n, num_trials, seed)` repeatedly draws `n` samples (with replacement) from `reward_pool`, takes each draw's max, and returns the average of those maxes over `num_trials` repetitions.
- `expected_best_of_n_reward` must never exceed `reward_pool`'s true maximum, and must be non-decreasing in expectation as `n` grows.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`expected_best_of_n_reward` is genuinely a MAX, not a mean, of each drawn sample — the whole point of best-of-N is that you get to pick the single best of your `n` attempts, not their average quality.

</details>

<details>
<summary>Hint 2</summary>

At `n=1`, best-of-`n` reduces to just picking a single random sample — so `expected_best_of_n_reward(pool, n=1, ...)` should converge (as `num_trials` grows) to `pool.mean()`, a useful sanity check on your Monte-Carlo loop.

</details>

## Theory

### The simple version

Imagine flipping a weighted coin many times and always reporting the LUCKIEST outcome you got, rather than a typical one — the more times you flip, the luckier your best-of-the-bunch result tends to be, but each additional flip helps less than the one before, since you're chasing an increasingly rare tail of the distribution. Best-of-N sampling applies exactly this idea to language model outputs: generate `N` candidates, report only the reward-model's favorite, and the quality of that favorite improves with `N` — but with diminishing returns, since eventually you're just re-sampling the SAME underlying distribution of possible responses.

### The formula

```text
best_of_n_select(responses, rewards) = (responses[argmax(rewards)], max(rewards))

expected_best_of_n_reward(pool, n, trials) = mean_{t=1..trials}( max(n samples drawn from pool) )
```

This is an ORDER STATISTIC (specifically, the expected value of the maximum of `n` i.i.d. draws) — it necessarily increases (or stays flat) as `n` grows, since adding more draws can only ever help the max, never hurt it, but the marginal gain from each additional draw shrinks as `n` gets large and the sampled max approaches the pool's true maximum.

### How PyTorch actually implements this

Context only, untested by your submission: best-of-N (often called "rejection sampling at inference time" or "reranking") is a widely-used, simple technique in production LLM systems — many API providers offer a "best of N completions" style parameter precisely because it reliably improves output quality using only extra COMPUTE at inference time, no additional training, retraining, or fine-tuning required at all.

## Explanation

`best_of_n_select` is a direct `argmax` over the rewards, returning both the winning response and its score.

`expected_best_of_n_reward` runs a genuine Monte-Carlo simulation: for each of `num_trials` repetitions, draw `n` samples (with replacement) from the given reward pool and record the maximum, then average those maxima — this exercise's `tests.py` confirms the result never exceeds the pool's true maximum, increases as `n` grows, shows genuinely diminishing returns (the first doubling of `n` helps more than a later doubling), is deterministic given a fixed seed, and at `n=1` converges to the pool's plain mean — a battery of checks that directly rule out a mutant that takes the MEAN of each draw instead of the MAX, which would make `expected_best_of_n_reward` completely insensitive to `n` (since the mean of `n` i.i.d. samples doesn't systematically increase with `n` the way a max does).
