---
name: vision-connected-components
title: Connected-Component Labeling
tags: [computer-vision, segmentation, graph-search]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A segmentation mask says which pixels are foreground, but not how many separate objects there are. **Connected-component labeling** assigns every foreground pixel to the object it belongs to: two pixels are in the same component if a path of foreground pixels links them. Using 4-connectivity, pixels touch only if they share an edge (up, down, left, right), and a diagonal contact does not connect them. The algorithm is a graph search: scan the image, and whenever you meet an unlabeled foreground pixel, start a flood fill (breadth-first search) that labels everything reachable. Component labels give object counts, areas and bounding boxes.

### From theory to code

Implement `label_components`.

### Constraints

- `binary` is a 2-D array of 0 and 1. Return `(labels, count)` where `labels` has the same shape, background is `0` and components are numbered `1..count`.
- Use **4-connectivity**.
- Number the components in the raster-scan order (row by row, left to right) of their first pixel.
- Use an explicit queue (breadth-first search) and do not use recursion, which would overflow on large components.

### Hints

<details>
<summary>Hint 1</summary>

When the scan finds an unlabeled foreground pixel, push it, label it and expand its four neighbours.

</details>

<details>
<summary>Hint 2</summary>

A `collections.deque` gives constant-time pops from the front.

</details>

## Theory

### The simple version

Colouring in islands on a map: pick an unpainted land cell, paint everything you can walk to without getting wet with a fresh colour, then continue scanning for unpainted land.

### The formula

$$
\text{components} = \text{connected components of the graph } G = (V, E),\; V = \{p : I(p) = 1\},\; E = \{(p, q) : |p - q|_1 = 1\}
$$

The search visits each pixel once, so the cost is $O(HW)$.

### How this is done in practice

`scipy.ndimage.label` and OpenCV's `connectedComponents` implement this (with two-pass union-find algorithms for speed). Component statistics drive object counting in microscopy, cleaning small blobs after segmentation and extracting instances from semantic masks.

## Explanation

The scan order fixes the labels deterministically, which is why the tests can compare entire label images. The diagonal test shows the practical difference between 4- and 8-connectivity.
