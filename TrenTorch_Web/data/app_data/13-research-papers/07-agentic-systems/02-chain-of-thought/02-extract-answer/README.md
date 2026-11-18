---
name: research-cot-extract-answer
title: 'Chain of Thought: Extracting the Final Answer'
tags: [research-papers, agents, reasoning, prompting]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Few-shot chain-of-thought outputs end with a fixed phrase. Parsing that phrase is how the evaluation pulls the final answer out of a long reasoning trace.

### From theory to code

Implement `extract_final_answer(text)`, returning the text after the last 'The answer is' phrase.

### Constraints

- Return None if the phrase does not occur.

### Hints

<details>
<summary>Hint 1</summary>

Use `re.findall` to capture the content after each phrase, then take the last match.

</details>

## Theory

### The simple version

Taking the last match matters: reasoning can mention the phrase on the way, but the final statement is the answer.

### The formula

$$a = \text{content after the last occurrence of ``The answer is''}$$

### How NumPy/PyTorch actually implements this

Benchmark evaluators apply the same pattern before comparing with the gold answer.

## Explanation

The capture stops at a period or newline, so trailing sentences are not included in the answer.
