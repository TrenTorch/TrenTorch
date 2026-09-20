---
name: agentic-learning-retrieve-similar-trajectories
title: Retrieve Past Trajectories for a Similar Task
tags: [agentic-systems, agent-learning, experience]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Once past trajectories are stored (see *Store Successful and Failed Agent Trajectories*), the next real question is finding the ones actually relevant to a *new* task. Unlike semantic retrieval over free text (see *Cosine-Similarity Top-K Retrieval From Scratch*), trajectories here are described by a small set of tags — "booking," "flight," "customer-support" — and similarity is just how many of those tags a stored trajectory shares with the new task, a simple integer overlap count rather than a continuous vector similarity.

### From theory to code

You're given `query_tags` (describing the new task) and every stored trajectory's `(trajectory_id, tags)`. Implement `find_similar_trajectories(query_tags, trajectories)`. Rank stored trajectories by how many tags they share with `query_tags`. Return **all** trajectory ids, sorted by overlap count descending, ties broken by ascending id.

### Constraints

- 0 to 500 stored trajectories; tags are plain strings, sets may be empty.

### Hints

<details>
<summary>Hint 1</summary>

Set intersection (`query_tags & tags`) directly gives you the shared tags; `len(...)` of that turns it into the overlap count this whole ranking is based on.

</details>

<details>
<summary>Hint 2</summary>

Sort by the tuple key `(-overlap_count, trajectory_id)` — the same "negate for descending, then break ties on id" pattern used for score-based rankings elsewhere in this curriculum.

</details>

## Theory

### The simple version

Count how many tags each stored trajectory shares with the new task's tags — a plain integer, not a continuous score — then sort everything by that count, highest first, breaking ties by id. Every stored trajectory gets ranked, even ones with zero overlap; the question doesn't ask you to filter, only to order.

### Why integer tag overlap instead of a continuous similarity score

Trajectories are naturally described by a handful of discrete tags rather than free text, so there's no embedding to compute a cosine similarity over — overlap count is the natural, honest similarity measure for this kind of categorical metadata, and it's exactly as simple as it looks: no hidden numerical subtlety, just set intersection size.

### How this shows up in real systems

Tag-based retrieval is a common, cheap complement to embedding-based retrieval in real experience-replay and case-based-reasoning systems — when items are naturally categorical (tagged by task type, tool used, domain), a direct overlap count is often both simpler to implement and easier to reason about than forcing everything through an embedding model.

## Explanation

The function computes each trajectory's overlap score with a set intersection, `len(query_tags & tags)`, in one comprehension over `trajectories` — this naturally handles an empty `query_tags` (every overlap comes out zero) and an empty `tags` set (same) without any special-casing. The scored list is then sorted once with the key `(-overlap, trajectory_id)`: negating the overlap count turns "higher overlap first" into an ascending sort, and including `trajectory_id` as the tuple's second element means it only ever breaks a genuine tie, exactly the same tie-break pattern used for other score-based rankings in this curriculum. The final list comprehension strips the score back off, returning just the ids in their now-fully-determined order.
