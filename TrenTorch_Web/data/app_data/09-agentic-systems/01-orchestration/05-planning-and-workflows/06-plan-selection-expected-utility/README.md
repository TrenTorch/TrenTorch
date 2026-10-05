---
name: agentic-plan-selection-expected-utility
title: Expected-Utility Plan Selection
tags: [agentic-systems, planning, decision-making, retries]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Often an agent has several candidate plans: a quick one that works 60% of the time, a thorough one that works 95% of the time but costs ten times as much. Choosing between them is decision-making under uncertainty, and the right yardstick is **expected utility**: the probability of success times the value of success, minus a weighted cost. Retries change the picture. If an attempt costs `c` and succeeds with probability `p`, trying up to `n` times raises the overall success probability to `1 - (1 - p)^n`, but you only pay for later attempts when earlier ones failed. A cheap unreliable plan with retries can beat an expensive reliable one.

### From theory to code

Implement `success_after_retries`, `expected_attempt_cost` and `select_plan`.

### Constraints

- `success_after_retries(p, n)` is `1 - (1 - p) ** n`.
- `expected_attempt_cost(p, cost, n)` is the expected total cost of up to `n` sequential attempts, paying `cost` for each attempt that is actually made: `cost * sum_{k=0}^{n-1} (1 - p) ** k`.
- `select_plan(plans, cost_weight)`: each plan is a dict with `p`, `value`, `cost` and `attempts`. Its utility is `value * success_after_retries(p, attempts) - cost_weight * expected_attempt_cost(p, cost, attempts)`. Return the index of the plan with the highest utility (lowest index on ties).

### Hints

<details>
<summary>Hint 1</summary>

The expected cost is a geometric series, but a short loop is clearer than the closed form here.

</details>

<details>
<summary>Hint 2</summary>

With `p = 1`, only the first attempt is ever paid for.

</details>

## Theory

### The simple version

Choosing between a cheap lottery ticket you can buy again and a costly sure thing: compare what you expect to win minus what you expect to spend, not the headline price.

### The formula

$$
P_{\text{succ}}(n) = 1 - (1-p)^n, \qquad \mathbb{E}[\text{cost}] = c\sum_{k=0}^{n-1}(1-p)^k, \qquad U = V\,P_{\text{succ}} - \lambda\,\mathbb{E}[\text{cost}]
$$

### How this is done in practice

Agent routers and cost-aware model cascades make the same trade-off: try a cheap model first and escalate on failure. The assumption of independent attempts is optimistic, since a hard task fails the same way each time, so measured retry success rates are used in practice.

## Explanation

Three small formulas that compose. The tests include a case where retrying a cheap plan beats a single attempt of an expensive one.
