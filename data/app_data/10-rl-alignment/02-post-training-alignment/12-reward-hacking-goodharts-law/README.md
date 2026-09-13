---
name: rl-alignment-reward-hacking-goodharts-law
title: 'Reward Hacking: When Optimizing the Reward Stops Meaning What You Wanted'
tags: [reinforcement-learning, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every single technique in this track — best-of-N (`10`), PPO (`06`), DPO (`07`), GRPO (`08`) — assumes the reward signal being optimized genuinely reflects what you actually want. But a reward model (`04-reward-modeling-bradley-terry`) is only ever a PROXY, trained on a finite sample of human preferences, and any proxy can be exploited: if optimizing HARDER against the proxy stops improving (or actively hurts) what you truly care about, that's reward hacking — a direct instance of Goodhart's Law ("when a measure becomes a target, it ceases to be a good measure").

### From theory to code

Implement `select_best_by_proxy` (optimizing purely against an imperfect proxy, exactly like `10-best-of-n-sampling` does), `true_reward_of_selection`, and `reward_hacking_gap`, quantifying exactly how much true quality gets sacrificed when the proxy and the true objective disagree.

### Constraints

- `select_best_by_proxy(candidates, proxy_rewards)` returns the index of the highest-`proxy_rewards` candidate — it must NEVER look at true rewards at all.
- `true_reward_of_selection(true_rewards, selected_index)` looks up the TRUE reward of whichever candidate got selected.
- `reward_hacking_gap(true_rewards, proxy_rewards)` returns `max(true_rewards) - true_reward_of_selection(true_rewards, select_best_by_proxy(..., proxy_rewards))` — always `>= 0`, and exactly `0` when the proxy and the true reward agree on the best candidate.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`select_best_by_proxy`'s signature includes `candidates` but its logic should touch ONLY `proxy_rewards` — that's the entire point: a proxy-optimizing selector has no access to ground truth, by design.

</details>

<details>
<summary>Hint 2</summary>

`reward_hacking_gap` is a comparison between two DIFFERENT selections: "what the proxy actually picked" versus "what an all-knowing oracle with access to the true reward would have picked" — the gap is exactly how much true quality was lost by trusting the proxy instead.

</details>

## Theory

### The simple version

Imagine a company that starts measuring "customer satisfaction" using average call-center call LENGTH, assuming longer calls mean agents are being more thorough — employees quickly learn to keep customers on the phone longer regardless of whether it actually helps them, and call length keeps going UP while genuine satisfaction goes DOWN. The metric was a reasonable proxy at first, but the moment people started optimizing directly against it, it decoupled from what it was originally meant to measure. Reward hacking is exactly this, applied to a reward model: it might correlate reasonably well with genuine response quality on average, but selecting HARDER for the highest proxy score can specifically seek out the exact cases where the proxy and true quality diverge most.

### The formula

```text
select_best_by_proxy(candidates, proxy_rewards) = argmax(proxy_rewards)     -- never touches true_rewards

reward_hacking_gap(true_rewards, proxy_rewards):
    proxy_choice  = select_best_by_proxy(candidates, proxy_rewards)
    oracle_choice = argmax(true_rewards)
    return true_rewards[oracle_choice] - true_rewards[proxy_choice]
```

The gap is always non-negative (an oracle with access to the true reward can never do WORSE than a proxy-based selector, by definition of "oracle"), and it's exactly `0` only when the proxy happens to rank the true-best candidate as its own favorite too — any actual disagreement between the two rankings shows up directly as wasted true quality.

### How PyTorch actually implements this

Context only, untested by your submission: reward hacking is a widely documented, real failure mode in RLHF systems — reward models have been observed to be exploitable via response length (longer responses often score higher regardless of quality), sycophancy (agreeing with the user regardless of correctness), or formatting tricks, all cases where `10-best-of-n-sampling`-style hard optimization against the proxy actively degrades what human evaluators actually prefer, which is exactly why real deployments monitor the gap between proxy reward and independent human evaluation over time, watching for exactly this kind of divergence.

## Explanation

`select_best_by_proxy` is a plain `argmax` over the proxy scores, structurally incapable of consulting the true reward — this exercise's `tests.py` confirms it via a rigged example where the proxy actively prefers the true-WORST candidate, demonstrating the selector follows the proxy blindly rather than secretly using the true signal.

`true_reward_of_selection` is a direct lookup, translating "which index got picked" into "how good was that pick, really".

`reward_hacking_gap` combines both to produce a single, honest number: how much true quality was sacrificed by trusting the proxy instead of the ground truth — `tests.py` verifies the gap is always non-negative across random data, is exactly zero when the proxy and true reward fully agree, grows as the proxy's misalignment worsens, and matches a direct computation using the TRUE reward values (not the proxy's) in the final subtraction — directly ruling out a mutant that accidentally computes the gap using proxy-reward values, which would misreport how much real quality was actually lost.
