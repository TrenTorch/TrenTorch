---
name: research-gorilla-retrieve-api
title: 'Gorilla: Retrieving the Right API'
tags: [research-papers, agents, tool-use, apis]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Gorilla (Patil et al., 2023) fine-tunes a model to call APIs and pairs it with a retriever that finds the relevant API documentation for each request. Retrieval keeps the model from inventing APIs that do not exist.

### From theory to code

Implement `retrieve_api(query, api_docs)`, returning the API whose description best overlaps the query.

### Constraints

- Overlap counts shared lowercase words.

### Hints

<details>
<summary>Hint 1</summary>

Split the query and each description into word sets, count shared words, and keep the best API in order.

</details>

## Theory

### The simple version

Grounding the call in a retrieved doc reduces hallucinated APIs. Word overlap is the simplest retriever; the paper uses embedding retrieval.

### The formula

$$\hat a = \arg\max_{a} \big|\,\text{words}(q) \cap \text{words}(\text{doc}_a)\,\big|$$

### How NumPy/PyTorch actually implements this

Gorilla's retriever returns the top API documents, which the model is then prompted with.

## Explanation

The first-listed tie rule keeps retrieval deterministic for evaluation.
