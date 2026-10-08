---
name: research-lookahead-sync-steps
title: 'Lookahead: When Syncs Happen'
tags: [research-papers, optimization, meta-optimizer]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Lookahead synchronizes only every k fast steps. Choosing k sets how often the slow weights are updated, with the fast optimizer running in between.

### From theory to code

Implement `sync_steps(total, k)`, the step numbers at which a sync happens.

### Constraints

- Steps are numbered from one.

### Hints

<details>
<summary>Hint 1</summary>

Keep each step whose number is a multiple of k.

</details>

## Theory

### The simple version

A large k gives the fast optimizer more room to explore before the slow weights move; a small k tracks it closely.

### The formula

$$\{t \in \{1,\ldots,T\} : t \bmod k = 0\}$$

### How NumPy/PyTorch actually implements this

Training loops check `step % k == 0` to decide when to sync.

## Explanation

The hand case: in steps 1 to 7 with k = 3, the sync steps are 3 and 6.
