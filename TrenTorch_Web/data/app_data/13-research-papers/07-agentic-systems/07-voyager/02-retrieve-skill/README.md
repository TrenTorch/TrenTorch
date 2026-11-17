---
name: research-voyager-retrieve-skill
title: 'Voyager: Retrieving a Skill'
tags: [research-papers, agents, embodied, skill-library]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Voyager does not put its whole skill library into the prompt. For each new task it retrieves the few skills most relevant to the task description, which keeps the context short as the library grows.

### From theory to code

Implement `retrieve_skill(library, query, score)`, returning the name of the best-matching skill.

### Constraints

- Return None for an empty library.

### Hints

<details>
<summary>Hint 1</summary>

Take the name with the maximum relevance score using `max` with a key function.

</details>

## Theory

### The simple version

Retrieval scales the library to thousands of skills without flooding the prompt. The relevance function can be embedding similarity in the real system.

### The formula

$$\hat s = \arg\max_{s \in L} \operatorname{score}(q, s)$$

### How NumPy/PyTorch actually implements this

Voyager retrieves skills by embedding similarity between the task and the skill descriptions.

## Explanation

The scoring function is a parameter, so the same retrieval logic works with keyword overlap or embeddings.
