---
name: vision-vit-info-nce
title: 'Stretch: InfoNCE Loss (CLIP-Style Contrastive Training)'
tags: [computer-vision, transformers, contrastive-learning]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Everything so far in this track trains a ViT to predict a fixed, predefined set of class labels. CLIP trains an image encoder and a text encoder _jointly_, with no fixed classes at all — instead, given a batch of `N` genuinely matched (image, caption) pairs, it asks a purely relative question: "out of these `N` captions, which one actually goes with this image?" Solving that N-way matching problem, for every image AND every caption in the batch simultaneously, forces both encoders to place matching image/text pairs near each other in a shared embedding space, and everything else far apart — with no manually-labeled classes needed at all, since the "labels" are just which pairs happened to arrive in the batch together.

### From theory to code

Theory says: normalize every embedding to unit length (so only direction, not magnitude, matters), compute the full `N x N` matrix of image-to-text similarities, and treat row `i` of that matrix as an `N`-way classification problem where the correct answer is always class `i` (image `i` matches text `i`). Do this in BOTH directions — image-to-text and text-to-image — since the two are different classification problems with different softmax normalizations, and average the two resulting losses.

Implement `info_nce_loss(image_embeds, text_embeds, temperature=0.07)` against that reasoning.

### Constraints

- `image_embeds`, `text_embeds`: both shape `(N, D)`. Row `i` of each is a matched pair — this is the key assumption; there is no separate labels argument because the matching is implicit in row order.
- `temperature`: positive float scaling similarities before softmax; smaller values sharpen the resulting distribution.
- Returns a single Python `float`: the average of the image-to-text and text-to-image cross-entropy losses.
- Neither `image_embeds` nor `text_embeds` are modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`image_embeds / np.linalg.norm(image_embeds, axis=1, keepdims=True)` L2-normalizes every row — do the same for `text_embeds`. After normalizing, a dot product between two rows equals their cosine similarity.

</details>

<details>
<summary>Hint 2</summary>

`logits = (image_norm @ text_norm.T) / temperature` gives the `(N, N)` similarity matrix. `labels = np.arange(N)` says "row i's correct match is column i." `cce_loss(softmax(logits), labels)` scores the image-to-text direction; `cce_loss(softmax(logits.T), labels)` scores text-to-image (transposing swaps which axis is being classified over). Average the two.

</details>

## Theory

### The simple version

Imagine a party game: everyone brought a photo and a caption, all photos go on one table and all captions on another, and each person has to correctly point at the caption that matches THEIR photo — while, at the same time, whoever brought that caption has to point back at the matching photo. InfoNCE is exactly this game turned into a loss function: every image gets scored against every caption in the batch (not just its own match), and the loss pushes the model to make the true match's score stand out from every other candidate's score, from both directions of the game at once.

### The formula

```text
image_norm = image_embeds / ||image_embeds||   (per row)
text_norm  = text_embeds  / ||text_embeds||    (per row)
logits     = (image_norm @ text_norm.T) / temperature       # (N, N)
labels     = [0, 1, ..., N-1]                                # row i's match is column i
loss       = (cce_loss(softmax(logits), labels)
              + cce_loss(softmax(logits.T), labels)) / 2
```

### How PyTorch actually implements this

CLIP's original training loop computes exactly this: `logits = image_embeds_norm @ text_embeds_norm.T * logit_scale` (where `logit_scale` is `1/temperature`, and is itself a _learned_ parameter rather than a fixed constant), then `(F.cross_entropy(logits, labels) + F.cross_entropy(logits.T, labels)) / 2` with `labels = torch.arange(N)`. This exercise reuses `01-classical-ml/02-classification`'s `softmax` and `cce_loss` rather than calling a fused `cross_entropy` directly, since that's exactly what this curriculum's earlier questions already built and verified — the two are mathematically the same computation, just split into two explicit steps here instead of one fused one.

## Explanation

Normalizing both embedding sets to unit length is what makes `image_norm @ text_norm.T` compute _cosine_ similarity rather than a raw, magnitude-sensitive dot product — this is essential, since otherwise the model could trivially "cheat" by just inflating embedding magnitudes rather than actually learning meaningful directions. Dividing by `temperature` rescales these bounded `[-1, 1]` cosine similarities before the softmax; a smaller temperature makes the softmax distribution sharper (more confident) for any given similarity gap, which is why lowering it drives already-correct predictions' loss further toward zero. `labels = np.arange(N)` encodes the batch's implicit ground truth directly from row order — no separate label array is needed because "the columns are literally the rows' matches" is baked into how the batch was constructed. Running `cce_loss` on `softmax(logits)` scores "does row i's highest similarity land on column i" (image-to-text), while running it on `softmax(logits.T)` performs the identical computation with rows and columns swapped (text-to-image) — since a similarity matrix isn't symmetric under softmax normalization (each row/column is normalized independently), these are genuinely two different losses, and averaging them is what makes the training signal push both directions of the matching problem simultaneously.
