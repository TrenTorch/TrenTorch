---
name: research-reflexion-success-rate
title: 'Reflexion: Measuring Success Across Trials'
tags: [research-papers, agents, memory, self-improvement]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Reflexion reports success rates across repeated trials on the same tasks, showing how much reflections improve the agent over attempts.

### From theory to code

Implement `success_rate(results)`, the fraction of successful attempts.

### Constraints

- Return 0.0 for an empty list.

### Hints

<details>
<summary>Hint 1</summary>

Count the truthy results and divide by the total.

</details>

## Theory

### The simple version

Comparing rates before and after reflection measures the effect of the memory, which is the paper's central claim.

### The formula

$$\text{SR} = \frac{1}{N}\sum_{i=1}^{N}\mathbb{1}[\text{success}_i]$$

### How NumPy/PyTorch actually implements this

Evaluation scripts report this rate per trial index to show the learning curve.

## Explanation

The guard for an empty list avoids dividing by zero when no trials have run yet.
