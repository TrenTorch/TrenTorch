---
name: research-voyager-add-skill
title: 'Voyager: Adding a Skill to the Library'
tags: [research-papers, agents, embodied, skill-library]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Voyager (Wang et al., 2023) builds a growing library of executable skills. Each skill is code the agent wrote and verified, stored under a name so it can be reused on later tasks.

### From theory to code

Implement `add_skill(library, name, code)`, returning a new library with the skill added.

### Constraints

- Do not modify the input library.

### Hints

<details>
<summary>Hint 1</summary>

Copy the dictionary, then set the new key.

</details>

## Theory

### The simple version

Immutable updates keep earlier library states available, which helps when a skill has to be rolled back after a bad addition.

### The formula

$$L' = L \cup \{\text{name} \mapsto \text{code}\}$$

### How NumPy/PyTorch actually implements this

Voyager's skill manager writes each verified program to a file keyed by its description.

## Explanation

Storing code rather than text lets the agent call the skill directly in later programs.
