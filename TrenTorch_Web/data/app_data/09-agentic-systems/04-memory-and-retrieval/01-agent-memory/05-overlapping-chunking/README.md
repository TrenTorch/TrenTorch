---
name: agentic-overlapping-chunking
title: Overlapping Chunking
tags: [agentic-systems, rag, chunking, retrieval]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Retrieval-augmented agents cannot embed a whole book at once, so documents are cut into **chunks**, each embedded and indexed separately. Chunk size is a trade-off: small chunks are precise but lose context, large chunks keep context but dilute the embedding with unrelated text. Cutting at fixed positions has a side effect: a sentence that straddles the boundary is split between two chunks and may be found in neither. **Overlap** repeats the last `overlap` tokens of each chunk at the start of the next, so that anything near a boundary appears whole in at least one chunk.

### From theory to code

Implement `chunk_tokens`.

### Constraints

- `tokens` is a list. `chunk_tokens(tokens, size, overlap)` returns a list of chunks (lists), with `0 <= overlap < size`.
- Chunks start at positions `0, size - overlap, 2 * (size - overlap), ...`. Each chunk is `tokens[start : start + size]`.
- Stop after the first chunk that reaches the end of the list, so no chunk consists only of tokens already covered by the previous one. An empty list gives `[]`.

### Hints

<details>
<summary>Hint 1</summary>

The stride is `size - overlap`.

</details>

<details>
<summary>Hint 2</summary>

A chunk reaches the end when `start + size >= len(tokens)`; make it the last one.

</details>

## Theory

### The simple version

Photocopying a long scroll in overlapping panels so that any sentence on a fold appears complete on at least one page.

### The formula

$$
\text{chunk}_j = t[\,j(s - o) : j(s - o) + s\,], \qquad \text{number of chunks} = \Big\lceil \frac{n - o}{s - o} \Big\rceil \;(n > s)
$$

### How this is done in practice

LangChain's `RecursiveCharacterTextSplitter` and LlamaIndex's node parsers add sentence and paragraph awareness on top of this, and chunk sizes of a few hundred tokens with 10 to 20% overlap are common defaults.

## Explanation

A strided loop with a careful stopping rule. The tests verify coverage (every token appears), the overlap itself and the absence of redundant tail chunks.
