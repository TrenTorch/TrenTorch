---
name: research-selfrefine-loop
title: 'Self-Refine: The Refinement Loop'
tags: [research-papers, agents, self-feedback, iterative]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Self-Refine (Madaan et al., 2023) has a single model produce a draft, critique it, and revise it, repeating until the critique is satisfied or a budget runs out. No extra training is needed.

### From theory to code

Implement `refine_loop(generate, feedback, refine, steps)`, running the draft, feedback and revision cycle.

### Constraints

- The feedback value 'OK' ends the loop.

### Hints

<details>
<summary>Hint 1</summary>

Generate once, then in each round check the feedback; stop on 'OK' or when the rounds run out, otherwise refine with the feedback.

</details>

## Theory

### The simple version

The model supplies its own critique, so improvement needs no external labels. The step budget bounds the cost when the critic never approves.

### The formula

$$y_{t+1} = \text{refine}(y_t, \text{feedback}(y_t)), \qquad \text{stop when feedback}(y_t) = \text{OK}$$

### How NumPy/PyTorch actually implements this

Self-Refine implementations run the same generate, feedback and refine prompts in this order.

## Explanation

The loop is the core of the method; the three functions are all calls to the same language model with different prompts.
