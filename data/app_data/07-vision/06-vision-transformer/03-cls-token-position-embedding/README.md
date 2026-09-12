---
name: vision-vit-cls-position-embedding
title: Class Token + Position Embedding
tags: [computer-vision, transformers, vision-transformer]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Two problems remain before a sequence of patch embeddings is ready for a transformer. First: attention has no built-in sense of "position" — it computes weighted averages over a *set* of vectors, so shuffling every patch in the sequence and running the exact same transformer would produce identically-shuffled output, with no way for the model to know patch 5 was originally in the top-right corner rather than the bottom-left. Second: a transformer produces one output vector *per input position* — for classification, something has to decide which position's final output actually represents "the whole image." ViT solves both with ideas borrowed directly from BERT: a learned position embedding added to every patch (fixing problem one), and a dedicated, learned "CLS token" prepended to the sequence, whose job is purely to end up holding a summary of the whole image after attention has let it look at every patch (fixing problem two).

### From theory to code

Theory says: prepend the (single, shared, learned) CLS token vector to the front of the patch embedding sequence, then add a learned position embedding — one vector per sequence position, including the CLS token's own position 0 — elementwise to the whole sequence.

Implement `add_cls_token_and_position_embedding(patch_embeddings, cls_token, position_embedding)` against that reasoning.

### Constraints

- `patch_embeddings`: shape `(num_patches, d_model)`.
- `cls_token`: shape `(1, d_model)`.
- `position_embedding`: shape `(num_patches + 1, d_model)`.
- Returns shape `(num_patches + 1, d_model)`.
- The CLS token occupies sequence position 0; the original patches follow in their original order at positions 1 through `num_patches`.
- None of the inputs are modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.concatenate([cls_token, patch_embeddings], axis=0)` stacks `cls_token` in front of `patch_embeddings` along the sequence axis, giving a `(num_patches + 1, d_model)` array.

</details>

<details>
<summary>Hint 2</summary>

Once concatenated, adding `position_embedding` is a plain elementwise addition — both arrays are now the same `(num_patches + 1, d_model)` shape.

</details>

## Theory

### The simple version

The CLS token is like an empty notepad handed to a new meeting attendee who has been told: "listen to everyone, and by the end of the meeting, write down your summary of what was said." It starts as a fixed, learned vector carrying no information about this specific image, but as it passes through each transformer block's attention, it gets to "listen to" (attend to) every patch's embedding — and by the final layer, its own vector has absorbed a summary of the entire image, ready to be handed to a classification head. Position embeddings solve a completely separate problem: since attention treats its input as an unordered set of vectors, adding a distinct, learned vector to each position is how the model gets told "this token is in position 3, not position 30" at all.

### The formula

```text
sequence = concatenate([cls_token, patch_embeddings], axis=0)   # (num_patches+1, d_model)
output   = sequence + position_embedding                         # elementwise, same shape
```

### How PyTorch actually implements this

In `nn.Module` terms, `cls_token` and `position_embedding` are both ordinary `nn.Parameter` tensors (learned via backpropagation exactly like any weight matrix), and the forward pass does exactly `torch.cat([cls_token.expand(batch_size, -1, -1), patch_embeds], dim=1) + position_embedding` — the only difference from this exercise is the extra batch dimension and the `.expand()` needed to broadcast one shared `cls_token` across every image in a batch. After the full transformer stack runs, real ViT classification heads take `output[:, 0, :]` — the CLS token's final position — exactly as this track's next question, `05-classification-head`, does.

## Explanation

`np.concatenate([cls_token, patch_embeddings], axis=0)` joins the two arrays along the sequence axis without modifying either — `cls_token`'s single row becomes position 0, and `patch_embeddings`' rows follow in their original order at positions 1 onward, exactly matching how BERT prepends its own `[CLS]` token ahead of a sentence's word tokens. Adding `position_embedding` afterward — not before — is what lets one shared `position_embedding` array correctly assign a distinct learned vector to every position INCLUDING the newly-prepended CLS token's position 0, since `position_embedding` was sized `(num_patches + 1, d_model)` specifically to cover that extra slot. Because addition is elementwise, this doesn't change WHICH information is in the sequence, only WHERE positional information gets baked directly into each token's own vector — a distinction that matters because, without it, attention downstream would have literally no way to distinguish two sequences that differ only in patch order.
