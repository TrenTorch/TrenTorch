---
name: research-googlenet-aux-loss
title: 'GoogLeNet: Auxiliary Classifier Loss'
tags: [research-papers, computer-vision, cnn, inception]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

GoogLeNet attaches two auxiliary classifiers to middle layers and adds their losses to the main loss with weight 0.3. The extra signal helps gradients reach the early layers of a very deep network.

### From theory to code

Implement `weighted_total_loss(main, aux, w)`, returning the main loss plus the weighted auxiliary loss.

### Constraints

- The default weight is 0.3, as in the paper.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the auxiliary loss by `w` and add it to the main loss.

</details>

## Theory

### The simple version

The auxiliary losses act as extra supervision for the middle of the network. Their weight is kept small so they guide training without dominating the final classifier.

### The formula

$$\mathcal{L} = \mathcal{L}_{\text{main}} + 0.3\,(\mathcal{L}_{\text{aux},1} + \mathcal{L}_{\text{aux},2})$$

### How NumPy/PyTorch actually implements this

Training scripts sum the main and auxiliary cross-entropies with this weight.

## Explanation

The paper discards the auxiliary heads at inference, so they add training cost but no test-time cost.
