---
name: agentic-cost-per-success-pareto
title: Cost per Success & Pareto Front
tags: [agentic-systems, evaluation, cost, pareto]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The best agent on a leaderboard may be the one nobody can afford to run. A fair comparison puts **cost** next to quality. **Cost per success** divides the total spend by the number of _successful_ tasks, so spending on failures counts against the agent. When comparing several configurations (different models, step budgets, prompts) it helps to find those that are **not dominated**: a configuration is dominated if another is at least as cheap and at least as successful, and strictly better in one of the two. The non-dominated set is the **Pareto front**, the only sensible choices, since every other configuration is beaten on both axes by something on the front.

### From theory to code

Implement `cost_per_success` and `pareto_front`.

### Constraints

- `cost_per_success(costs, successes)`: `costs` is a list of per-task costs and `successes` a list of booleans of the same length. Return `sum(costs) / (number of successes)`, or `float('inf')` if there are no successes.
- `pareto_front(points)`: `points` is a list of `(cost, success_rate)` pairs. Point `i` is **dominated** if some other point `j` has `cost_j <= cost_i` and `rate_j >= rate_i` with at least one inequality strict. Return the sorted list of indices of non-dominated points. Identical duplicate points do not dominate each other.

### Hints

<details>
<summary>Hint 1</summary>

Failures still add to the numerator: `sum(costs)` includes every task.

</details>

<details>
<summary>Hint 2</summary>

A quadratic loop over pairs is fine for the handful of configurations being compared.

</details>

## Theory

### The simple version

Choosing a car by comparing price and reliability: any model that is both pricier and less reliable than another is simply not worth considering. What remains is the real trade-off.

### The formula

$$
\text{CPS} = \frac{\sum_{t} c_t}{\sum_t s_t}, \qquad
i \text{ dominated} \iff \exists j:\ c_j \le c_i \wedge r_j \ge r_i \wedge (c_j < c_i \vee r_j > r_i)
$$

### How this is done in practice

Agent leaderboards increasingly publish cost and accuracy together (for example Pareto plots on the HAL and SWE-bench-style agent evaluations) because cheap baselines with retries can match expensive agents. Tokens, tool-call fees and wall-clock time are all possible cost axes.

## Explanation

A ratio that is honest about failures and a dominance check that is easy to get wrong with equal points. The tests cover the infinite-cost case and duplicates.
