---
name: production-multimodal-route-modality-for-question
title: Route a Question to the Right Modality
tags: [production-systems, multimodal, routing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A question about a document can be about its text, an embedded image, or a table -- and answering it well usually means retrieving from the specific modality it's actually asking about, rather than searching everything indiscriminately every time.

### The task

Write `route_modality_for_question(question, modality_keywords, default_modality)`, where `modality_keywords` maps a modality name to a list of keywords. Return the first modality (in dict order) with a case-insensitive keyword match in the question, or `default_modality` if none match.

## Theory

### The simple version

This is the same keyword-triage idea used elsewhere in this curriculum for routing and classification, applied to modality selection: a question mentioning "chart" or "picture" is almost certainly asking about an image; one mentioning "row" or "column" is almost certainly asking about a table.

### Why a default modality, not "no match found"

Most questions about a document are plain text questions and won't mention any modality-specific keyword at all -- "what's the deadline mentioned in this document" doesn't say "text" anywhere. Falling back to a sensible default (text, ordinarily the most common modality) rather than erroring keeps the router usable for the common case, while still routing the recognizable minority precisely.

### How this shows up in real systems

A production multimodal QA system typically classifies a question's likely modality before retrieval, so it can search the image index for image-shaped questions and the text index for everything else, instead of paying the cost of searching every modality on every single query.

## Explanation

Modalities are checked in the order `modality_keywords` was given, and the first one with any matching keyword wins -- which is why a question mentioning both an image keyword and a table keyword resolves to whichever modality was declared first, not the one with more matches. No match at all falls through to `default_modality`.
