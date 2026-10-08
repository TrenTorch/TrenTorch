---
name: research-gpt3-few-shot-prompt
title: 'GPT-3: Building a Few-Shot Prompt'
tags: [research-papers, transformers, llm, llm, prompting]
difficulty: Beginner
---

## Statement

### The problem, from first principles

GPT-3 (Brown et al., 2020) performed tasks from a few examples placed in the prompt, with no weight updates. The prompt is just text: a few solved input-output pairs, then the new input with its answer left blank for the model to fill in.

### From theory to code

Implement `build_few_shot_prompt(examples, query, sep)`, which formats each example as `input => output`, appends `query =>`, and joins everything with `sep`.

### Constraints

- With no examples the prompt is only the query.

### Hints

<details>
<summary>Hint 1</summary>

Build a list of formatted strings, add the query as the last item, then join with the separator.

</details>

## Theory

### The simple version

The model continues the pattern it sees. Showing solved examples fixes the format and the task, so the final blank is completed the same way.

### The formula

$$\text{prompt} = [\,x_1 \Rightarrow y_1,\ \ldots,\ x_k \Rightarrow y_k,\ x \Rightarrow\,]$$

### How NumPy/PyTorch actually implements this

Prompt templates in LLM libraries perform the same string assembly before tokenization.

## Explanation

This is in-context learning: the examples change the model's behavior at inference time only through the text it conditions on.
