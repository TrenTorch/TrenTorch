---
name: research-selfrefine-first-ok
title: 'Self-Refine: The First Accepted Round'
tags: [research-papers, agents, self-feedback, iterative]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The refinement loop stops at the first round the critic approves. Recording that round tells you how many revisions were needed.

### From theory to code

Implement `first_ok_index(feedbacks)`, returning the round at which the draft was accepted.

### Constraints

- Match 'OK' exactly.

### Hints

<details>
<summary>Hint 1</summary>

Scan the feedback list for the first exact 'OK'.

</details>

## Theory

### The simple version

The round count measures how much refinement a task needed, which is useful when comparing the cost of the loop against single-pass generation.

### The formula

$$r^* = \min\{t : \text{feedback}_t = \text{OK}\}$$

### How NumPy/PyTorch actually implements this

Evaluation scripts log the accepting round per task to report refinement cost.

## Explanation

Exact matching avoids accepting a critique that merely contains the word OK.
