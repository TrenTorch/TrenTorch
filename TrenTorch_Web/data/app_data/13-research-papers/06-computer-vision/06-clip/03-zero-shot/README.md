---
name: research-clip-zero-shot
title: 'CLIP: Zero-shot Classification'
tags: [research-papers, computer-vision, vision-language, contrastive]
difficulty: Beginner
---

## Statement

### The problem, from first principles

CLIP can classify images it was never trained on. Each class name is turned into a text prompt, and the image is assigned to the prompt it is most similar to. No labelled training data for the new classes is needed.

### From theory to code

Implement `zero_shot_predict(img_emb, class_embs)`, returning the index of the best-matching class prompt.

### Constraints

- Returns a Python int.

### Hints

<details>
<summary>Hint 1</summary>

Normalize the image and class embeddings, compute all the cosine similarities, then take the argmax.

</details>

## Theory

### The simple version

The text encoder turns class names into classifier weights, so the set of classes can change at test time without retraining.

### The formula

$$\hat y = \arg\max_c \cos\big(f_{\text{img}}(x),\, f_{\text{txt}}(\text{prompt}_c)\big)$$

### How NumPy/PyTorch actually implements this

CLIP zero-shot evaluation computes this argmax for every test image against the class prompts.

## Explanation

Normalization makes the argmax depend only on direction, the same geometry the contrastive training used.
