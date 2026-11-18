---
name: research-moco-enqueue
title: 'MoCo: The Key Queue'
tags: [research-papers, unsupervised, contrastive, momentum]
difficulty: Beginner
---

## Statement

### The problem, from first principles

MoCo keeps a fixed-size first-in, first-out queue of keys from past batches. Each training step pushes the newest keys in and drops the oldest, so the negatives are always from recent batches.

### From theory to code

Implement `enqueue(queue, new_keys, K)`, which returns the queue with the new keys appended and capped at `K` entries.

### Constraints

- The queue keeps the most recent `K` rows.

### Hints

<details>
<summary>Hint 1</summary>

Concatenate the new keys after the queue, then keep the last `K` rows.

</details>

## Theory

### The simple version

The queue decouples the number of negatives from the batch size. A large K gives many negatives without needing a large batch on the device.

### The formula

$$Q \leftarrow \text{concat}(Q, K_{\text{batch}})[-K:]$$

### How NumPy/PyTorch actually implements this

MoCo implementations maintain the queue as a tensor with a pointer that wraps around, which has the same effect.

## Explanation

The slice keeps exactly K rows, so the queue has constant memory.
