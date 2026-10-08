---
name: research-selfrefine-prompt
title: 'Self-Refine: The Refinement Prompt'
tags: [research-papers, agents, self-feedback, iterative]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Self-Refine's refinement prompt gives the model the task, its own previous draft and the critique, then asks for a revision. Showing the draft is what makes the revision a targeted edit.

### From theory to code

Implement `build_refine_prompt(task, draft, feedback)`, returning the revision request.

### Constraints

- The prompt ends with the rewrite instruction.

### Hints

<details>
<summary>Hint 1</summary>

Format the three inputs with labels, then add the instruction.

</details>

## Theory

### The simple version

Including the previous draft lets the model change only what the feedback targets, instead of starting from scratch.

### The formula

$$\text{prompt} = [\,\text{task},\ y_t,\ \text{feedback}_t,\ \text{``rewrite''}\,]$$

### How NumPy/PyTorch actually implements this

Refinement prompt templates in the paper follow this same task, draft and feedback layout.

## Explanation

The revision request is a fixed template filled per round, so the loop is easy to audit.
