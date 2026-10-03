---
name: agentic-tool-selection
title: Tool Retrieval
tags: [agentic-systems, tools, retrieval, tf-idf]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

An agent with hundreds of tools cannot put every description in the prompt: it would burn the context window and confuse the model. The scalable approach is **tool retrieval**: embed the user's request and each tool's description, rank the tools by similarity and show the model only the top few. Even without a neural embedding, classic **TF-IDF** gives a strong baseline. Words that appear in few tool descriptions ("invoice", "weather") carry more weight than words that appear in all of them ("get", "data"), and the cosine similarity between the weighted query and description vectors ranks the tools.

### From theory to code

Implement `rank_tools`.

### Constraints

- `tools` maps tool names to description strings. Tokenize with `re.findall(r'[a-z0-9]+', text.lower())`.
- Inverse document frequency over the descriptions only: `idf(w) = log((N + 1) / (df(w) + 1)) + 1` where `N` is the number of tools and `df(w)` the number of descriptions containing `w`. Words absent from every description still get `df = 0`.
- The vector for a text is its term counts multiplied by `idf`. Score each tool by the cosine similarity between the query vector and the description vector (`0.0` if either has zero norm).
- Return the names of the `top_k` highest scoring tools, sorted by score descending and then by name ascending.

### Hints

<details>
<summary>Hint 1</summary>

Build one shared vocabulary from the query and all descriptions.

</details>

<details>
<summary>Hint 2</summary>

Compute `df` once from the descriptions, then reuse it for the query.

</details>

## Theory

### The simple version

A librarian finding the right reference book for your question: rare, telling words in the question ("amortization") narrow the shelf far more than common ones ("how", "to").

### The formula

$$
\text{idf}(w) = \ln\frac{N + 1}{\text{df}(w) + 1} + 1, \qquad
\text{score}(q, d) = \frac{\mathbf{v}_q \cdot \mathbf{v}_d}{\lVert \mathbf{v}_q\rVert\,\lVert\mathbf{v}_d\rVert}, \quad \mathbf{v}_{t,w} = \text{tf}_{t}(w)\,\text{idf}(w)
$$

### How this is done in practice

Frameworks implement this with dense embeddings and a vector index, and re-rank candidates with the model. The Model Context Protocol's `tools/list` can return many tools, which makes retrieval necessary on large servers.

## Explanation

The whole pipeline is tokenization, idf, weighted counts and cosine. Ties are broken by name so that results are reproducible.
