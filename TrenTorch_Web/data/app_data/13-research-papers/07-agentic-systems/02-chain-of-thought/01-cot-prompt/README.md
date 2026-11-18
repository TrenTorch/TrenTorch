---
name: research-cot-prompt
title: 'Chain of Thought: Few-shot Prompt With Reasoning'
tags: [research-papers, agents, reasoning, prompting]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Chain-of-thought prompting (Wei et al., 2022) shows the model worked examples in which the answer is preceded by its reasoning. The model then reasons step by step on the new question, which improves accuracy on arithmetic and logic tasks.

### From theory to code

Implement `build_cot_prompt(examples, question)`, formatting the demonstrations and the new question.

### Constraints

- Each example includes its reasoning before the answer.

### Hints

<details>
<summary>Hint 1</summary>

Format each example as Q, A with reasoning and 'The answer is', then add the new question with an empty answer.

</details>

## Theory

### The simple version

The reasoning in the examples is what the model imitates. Without it, the model tends to jump straight to an answer that is often wrong.

### The formula

$$\text{prompt} = [\,(q_i, r_i, a_i)\,]_{i=1}^{k} \,\|\, (q, \text{``A:''})$$

### How NumPy/PyTorch actually implements this

Evaluation harnesses build the same prompt template from exemplar sets for each benchmark.

## Explanation

The few-shot format keeps the demonstrations and the query in the same shape so the model continues the pattern.
