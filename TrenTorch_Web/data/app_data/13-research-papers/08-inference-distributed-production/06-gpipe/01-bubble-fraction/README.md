---
name: research-gpipe-bubble-fraction
title: 'GPipe: The Pipeline Bubble'
tags: [research-papers, systems, parallelism, pipeline]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

GPipe (Huang et al., 2019) splits a model into pipeline stages on different devices and feeds each step as micro-batches. At the start and end, some stages wait for work. That idle time is the bubble.

### From theory to code

Implement `pipeline_bubble_fraction(stages, micro)`, returning the idle fraction of a pipeline step.

### Constraints

- Return a float.

### Hints

<details>
<summary>Hint 1</summary>

The schedule has `M + S - 1` time slots per stage, of which `S - 1` are idle on each device; divide.

</details>

## Theory

### The simple version

More micro-batches per step fill the pipeline more fully, so the bubble shrinks. The paper pairs pipelining with micro-batching for this reason.

### The formula

$$\text{bubble} = \frac{S-1}{M+S-1}$$

### How NumPy/PyTorch actually implements this

Pipeline schedulers in training frameworks report this bubble fraction for a chosen micro-batch count.

## Explanation

The formula counts the warm-up and drain slots, which are the idle ones when stages wait on each other.
