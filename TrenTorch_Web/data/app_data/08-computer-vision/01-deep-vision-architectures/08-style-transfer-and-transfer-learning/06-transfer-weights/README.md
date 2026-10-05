---
name: vision-transfer-weights
title: Pretrained Weight Transfer
tags: [computer-vision, transfer-learning, state-dict, fine-tuning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

To fine-tune a pretrained model for a new task you usually keep the **backbone** and replace the **head**: an ImageNet classifier has a 1000-way output layer, but your dataset has 10 classes. Loading the pretrained checkpoint straight into the new model would crash on the mismatched head. The standard recipe copies every pretrained tensor whose **name and shape both match** the new model, leaves the others at their fresh initialization, and reports what was copied and what was skipped. The report is not decoration: silently skipping a backbone layer because of a naming change is a common bug that makes "pretrained" training behave like training from scratch.

### From theory to code

Implement `transfer_weights`.

### Constraints

- `src` and `dst` are dicts mapping parameter names to NumPy arrays (like state dicts). Return `(new_dst, copied, skipped)`.
- For each name in `dst`: if the name is in `src` **and** the shapes are equal, `new_dst[name]` is a copy of `src[name]` and the name is in `copied`; otherwise `new_dst[name]` is a copy of `dst[name]` and the name is in `skipped`.
- `copied` and `skipped` are alphabetically sorted lists. Names present only in `src` are ignored. Neither input dict nor array is modified, and the returned arrays are copies.

### Hints

<details>
<summary>Hint 1</summary>

`np.array(x, copy=True)` makes an independent copy.

</details>

<details>
<summary>Hint 2</summary>

A matching name with a different shape (a resized head) goes to `skipped`.

</details>

## Theory

### The simple version

Moving into a new house with the old furniture: pieces that fit the new rooms come along, pieces that no longer fit are replaced, and you keep a list of what was left behind.

### The formula

$$
\theta'_k = \begin{cases} \theta^{\text{src}}_k & k \in \text{src} \wedge \text{shape}(\theta^{\text{src}}_k) = \text{shape}(\theta^{\text{dst}}_k) \\ \theta^{\text{dst}}_k & \text{otherwise}\end{cases}
$$

### How this is done in practice

PyTorch's `load_state_dict(strict=False)` returns `missing_keys` and `unexpected_keys`, and timm's `load_pretrained` filters mismatched heads this way. Printing the skipped names is the quickest sanity check that a fine-tuning run really started from the pretrained weights.

## Explanation

A single loop with two conditions. Returning copies keeps the pretrained checkpoint intact so it can be reused for another run.
