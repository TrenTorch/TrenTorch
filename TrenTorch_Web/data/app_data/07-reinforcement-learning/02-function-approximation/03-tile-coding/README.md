---
title: Tile Coding Features
name: rl-tile-coding
difficulty: Advanced
tags: [rl, features, tile-coding, approximation]
---

## Statement

Tile coding creates binary feature vectors by dividing the state space into overlapping tiles. Each tile is a feature (1 if state falls in tile, 0 otherwise).

### The problem, from first principles

Polynomials don't scale to high-dim spaces. Tile coding works by creating multiple overlapping grids and activating tiles the state falls into. Simple, sparse, and effective.

### From theory to code

Implement `tile_coding(state, num_tilings, num_tiles)` which:
- Takes 1D state in [0, 1]
- Creates num_tilings overlapping grids
- Each grid has num_tiles tiles
- Returns binary feature vector (indices of active tiles)

### Constraints

- state in [0, 1]
- num_tilings >= 1
- num_tiles >= 2
- Return indices of active tiles (sparse representation)

### Hints

<details>
<summary>Hint 1: Grid resolution</summary>
Each tiling divides [0,1] into num_tiles equally spaced buckets.
</summary>

<details>
<summary>Hint 2: Overlapping</summary>
Offset each tiling by 1/(num_tilings * num_tiles) for overlap.
</details>

<details>
<summary>Hint 3: Sparse representation</summary>
Return only active tile indices, not dense vector.
</details>

## Theory

### The simple version

Divide state space into overlapping grids. State activates the tile it falls into on each grid. Features are sparse binary vectors.

### Why it works

Generalization: nearby states share tiles, so they get similar values. Sparse: only num_tilings active features per state, not num_tiles.

### Tile coding properties

- Sparse: O(num_tilings) active features
- Local generalization: similar states share features
- Works in high dimensions (tile each dimension independently)

## Explanation

Tile coding is a workhorse of traditional RL. Deep RL mostly replaced it, but tile coding is simpler, faster, and interpretable. Good choice for lower-dim problems.
