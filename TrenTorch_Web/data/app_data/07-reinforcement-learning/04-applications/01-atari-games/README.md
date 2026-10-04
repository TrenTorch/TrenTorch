---
title: Atari Game Playing
name: rl-atari-games
difficulty: Advanced
tags: [rl, applications, deep-rl, vision]
---

## Statement

Apply DQN to Atari games: convert pixel observations to feature vectors, train on massive replay buffers, achieve superhuman performance.

### The problem, from first principles

Raw pixels as state: 84x84x4 = 28,224 inputs per frame. Fully connected networks fail. Convolutional networks extract features. DQN learns to play from pixels alone.

### From theory to code

Implement `preprocess_atari_frame(raw_frame)` which:
- Takes raw 210x160x3 RGB frame
- Crops to 160x160
- Resizes to 84x84
- Converts to grayscale
- Normalizes to [0, 1]
- Returns preprocessed frame

### Constraints

- Input: 210x160x3 uint8 Atari frame
- Output: 84x84 float32 frame
- Use standard preprocessing

### Hints

<details>
<summary>Hint 1: Grayscale</summary>
0.299*R + 0.587*G + 0.114*B
</details>

<details>
<summary>Hint 2: Resize</summary>
Bilinear interpolation or max-pool
</details>

<details>
<summary>Hint 3: Normalize</summary>
frame / 255.0
</details>

## Theory

### Vision in RL

Raw pixels are high-dimensional but redundant. Preprocessing:
1. Grayscale: color usually irrelevant
2. Resize: 84x84 is standard (Atari)
3. Normalize: improves learning

### Frame stacking

One frame insufficient (can't infer velocity). Stack 4 frames: [t-3, t-2, t-1, t].

### DQN on Atari

Massive replay buffer (1M transitions), target network update every 10k steps, long training (40M frames). Result: superhuman on 40+ games.

## Explanation

Atari was the proof that deep RL could work. One algorithm (DQN), one architecture (CNN), zero domain knowledge, superhuman performance on dozens of games.
