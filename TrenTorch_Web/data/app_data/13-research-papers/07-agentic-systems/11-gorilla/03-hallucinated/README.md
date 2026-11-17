---
name: research-gorilla-hallucinated
title: 'Gorilla: Detecting Hallucinated APIs'
tags: [research-papers, agents, tool-use, apis]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Models can invent APIs that sound plausible. Gorilla's evaluation counts such hallucinations separately, because a made-up function fails at runtime even when the call looks well formed.

### From theory to code

Implement `is_hallucinated(call_name, api_list)`, returning True when the called API is not known.

### Constraints

- Match names exactly.

### Hints

<details>
<summary>Hint 1</summary>

Check whether the name is absent from the list of known APIs.

</details>

## Theory

### The simple version

Flagging hallucinations before execution prevents failed calls and gives a measurable error category for evaluation.

### The formula

$$\text{hallucinated} \iff \text{name} \notin \mathcal{A}_{\text{known}}$$

### How NumPy/PyTorch actually implements this

Evaluation harnesses report this rate separately from argument errors.

## Explanation

The known list is the API catalogue the retriever searches, so the check is consistent with retrieval.
