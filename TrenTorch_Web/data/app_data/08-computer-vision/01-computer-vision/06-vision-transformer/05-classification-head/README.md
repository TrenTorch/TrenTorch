---
name: vision-vit-classification-head
title: Classification Head
tags: [computer-vision, transformers, vision-transformer]
difficulty: Beginner
---

## Statement

### The problem, from first principles

After the transformer block runs, the sequence still has `seq_len` positions — one for the CLS token, one per patch. For whole-image classification, only one final number per class is wanted, not one per sequence position. Everything from `03-cls-token-position-embedding` onward was specifically designed to funnel a summary of the entire image into the CLS token's position through attention, which is exactly why classification only ever looks at that one position and throws every patch position's final output away.

### From theory to code

Theory says: take the CLS token's final representation (position 0 of the transformer's output sequence), run it through a linear layer mapping `d_model` to `num_classes`, then softmax to turn the resulting logits into a probability distribution over classes — the exact same classification pipeline `01-classical-ml/02-classification` already built, just fed a learned feature vector instead of raw tabular features.

Implement `classification_head(sequence, weight, bias)` against that reasoning.

### Constraints

- `sequence`: shape `(seq_len, d_model)` — the transformer block's output.
- `weight`: shape `(num_classes, d_model)`. `bias`: shape `(num_classes,)`.
- Returns shape `(num_classes,)`: a probability distribution (non-negative, summing to 1).
- Only `sequence[0]` (the CLS token) affects the output — every other position is ignored entirely.
- `sequence`, `weight` and `bias` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`sequence[0]` pulls out the CLS token's row, shape `(d_model,)` — but `linear` and `softmax` both expect a 2D `(batch, features)` input, so wrap it as `sequence[0][None, :]` (or equivalently `sequence[0:1]`) to get shape `(1, d_model)`.

</details>

<details>
<summary>Hint 2</summary>

`softmax(linear(cls_token_row, weight, bias))` returns shape `(1, num_classes)` — index `[0]` on the result to get the plain `(num_classes,)` vector this question asks for.

</details>

## Theory

### The simple version

Picture the CLS token as a designated note-taker who sat through an entire meeting (attending to every patch through the transformer's attention), and at the end, everyone else in the meeting goes home — only the note-taker's final summary gets handed to the decision-maker. The classification head IS the decision-maker: it takes that one summary vector and converts it into "how confident am I this image belongs to each possible class," using nothing more than the same linear-plus-softmax pipeline any classifier — image, tabular, or otherwise — ultimately reduces to.

### The formula

```text
cls_output = sequence[0]                              # (d_model,)
logits     = linear(cls_output, weight, bias)         # (num_classes,)
probs      = softmax(logits)                          # (num_classes,), sums to 1
```

### How PyTorch actually implements this

`torchvision.models.vit_b_16` and every other real ViT implementation take exactly `sequence_output[:, 0, :]` (the CLS token across the batch dimension) and feed it into a single `nn.Linear(d_model, num_classes)` — `nn.CrossEntropyLoss` then fuses the softmax and the loss computation together during training for numerical stability, the same fusion `01-classical-ml/02-classification`'s own softmax-plus-cross-entropy questions already discuss. It's worth noticing there is nothing vision-specific about this final step either: it's the identical classification head architecture BERT uses for sentence-level classification tasks, applied to the identical idea of "a CLS token summarizing an entire input."

## Explanation

`sequence[0]` selects the CLS token's row specifically because every earlier step in this track was designed around exactly that convention: `03-cls-token-position-embedding` placed it at position 0, and the transformer block's attention (`04-vit-encoder-block`) let it accumulate information from every patch over the course of the network. `linear(cls_output, weight, bias)` maps this `d_model`-dimensional summary into `num_classes` raw scores (logits) — one per possible class, with no constraint yet on their range or relative scale. `softmax` then normalizes those logits into a genuine probability distribution: exponentiating makes every value positive, and dividing by the sum forces the whole vector to sum to exactly 1, giving a properly interpretable "confidence in each class" output — and because only `sequence[0]` was ever read, every other position's final transformer output plays no role in the classification decision whatsoever.
