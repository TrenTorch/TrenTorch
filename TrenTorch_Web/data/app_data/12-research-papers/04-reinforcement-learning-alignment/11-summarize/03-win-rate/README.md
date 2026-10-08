---
name: research-summarize-win-rate
title: 'Learning to Summarize: The Win Rate'
tags: [research-papers, reinforcement-learning, alignment, rlhf, summarization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The paper compares summaries by win rate: how often a human or model prefers one system's summary over another's. Counting ties as half a win makes the metric symmetric when two systems are tied.

### From theory to code

Implement `win_rate(a, b)`, returning the fraction of prompts where `a` beats `b`, with ties counting half.

### Constraints

- Both score arrays cover the same prompts.

### Hints

<details>
<summary>Hint 1</summary>

Average the strict wins and add half the average of the ties.

</details>

## Theory

### The simple version

A win rate near one half means the systems are indistinguishable. Ties are split evenly so that comparing a system with itself gives exactly one half.

### The formula

$$\text{WR}(A, B) = \frac{1}{N}\Big(\#\{a_i > b_i\} + \tfrac{1}{2}\#\{a_i = b_i\}\Big)$$

### How NumPy/PyTorch actually implements this

Evaluation scripts count these outcomes per prompt and report the ratio.

## Explanation

The formula is the standard pairwise accuracy with ties split, used throughout the paper's evaluation.
