---
name: research-reflexion-prompt
title: 'Reflexion: The Reflection Prompt'
tags: [research-papers, agents, memory, self-improvement]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Reflexion asks the model to write a reflection after a failed attempt. The prompt gives the task, the trajectory and the environment feedback, then requests a plan for next time.

### From theory to code

Implement `build_reflection_prompt(task, trajectory, feedback)`, returning the reflection request.

### Constraints

- The prompt ends with the reflection instruction.

### Hints

<details>
<summary>Hint 1</summary>

Format the three inputs with their labels, then append the instruction.

</details>

## Theory

### The simple version

Concrete feedback and the actual trajectory let the model point at the step that failed. A vague prompt yields generic advice that does not help the next attempt.

### The formula

$$\text{reflection} = \text{LLM}(\text{task}, \text{trajectory}, \text{feedback}, \text{instruction})$$

### How NumPy/PyTorch actually implements this

Reflexion code prompts follow this template with a fixed reflection instruction.

## Explanation

The reflection is stored and included in the next attempt's prompt, which is the verbal reinforcement the paper describes.
