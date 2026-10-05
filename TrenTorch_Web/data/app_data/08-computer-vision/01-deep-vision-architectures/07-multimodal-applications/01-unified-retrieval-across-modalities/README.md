---
name: production-multimodal-unified-retrieval
title: Unified Retrieval Across Text and Image-Caption Chunks
tags: [production-systems, multimodal, retrieval]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A multimodal knowledge base doesn't store only paragraphs of text -- an image gets indexed by its caption or a generated description, a chart by a summary of what it shows. A query shouldn't need to know in advance whether the most relevant piece of content happens to be a paragraph or an image's caption; retrieval should treat both as equally eligible answers.

### The task

Write `retrieve_across_modalities(chunks, query_keywords)`, where each chunk is `(chunk_id, modality, text)`. Score every chunk by how many keywords match its text, case-insensitively, regardless of its modality, and return the ids of chunks with a positive score, ranked by score descending with ties broken by original order.

## Theory

### The simple version

Keyword-match scoring works the same way whether the text underneath is a paragraph pulled from a document or a one-line caption generated for an image -- both are just text once they've been indexed, so the retrieval logic never needs to branch on modality.

### Why "unified" specifically means no special-casing

A retrieval function that scores text chunks one way and image-caption chunks another way (a bonus for one, a penalty for the other) has quietly baked in an assumption about which modality is more trustworthy or relevant -- an assumption the query itself never stated. Treating every chunk's text identically, and only ever tagging the underlying modality as metadata rather than a scoring factor, keeps retrieval genuinely modality-agnostic.

### How this shows up in real systems

This is how a real multimodal RAG index behaves: images, tables, and text are all converted to a common representation (captions, descriptions, or embeddings) at ingestion time, so retrieval at query time is a single unified ranking over everything, not three separate searches stitched together afterward.

## Explanation

Every chunk's text is scored the same way regardless of its modality tag -- modality is carried through only as metadata, never consulted by the scoring itself. Chunks are ranked by score descending, with original order breaking ties, and chunks scoring zero are dropped since they matched nothing about the query at all.
