---
name: lm-average-nll
title: Average Negative Log-Likelihood
tags: [language-modeling, evaluation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Having built a model, how good is it? The honest question is how much probability it gave to what actually happened. For one word, multiply the probability of each step: a pair that the model finds likely contributes a number near one and a pair it finds unlikely contributes a number near zero. Products of many small numbers underflow, so we take logs and add. Flipping the sign gives the **negative log-likelihood** (NLL), where lower is better, and dividing by the number of steps makes models comparable across datasets of different sizes. A model that knows nothing and spreads probability evenly over `V` symbols scores exactly `ln V`, so that number is the bar any real model should beat.

### From theory to code

Implement `average_nll(words, probs, itos)`, the mean negative log-probability that the model assigns to every adjacent pair in the wrapped words.

### Constraints

- `probs` is a row-stochastic `(V, V)` array where `probs[i, j]` is the probability of `itos[j]` after `itos[i]`. `itos[0]` is the boundary symbol `.`.
- Wrap each word as `.` + word + `.`. Every adjacent pair counts once, including the pairs touching the boundary.
- Return the mean of `-log(probs[i, j])` over all pairs in all words, as a float. Use the natural logarithm.
- If a pair has probability exactly 0 the result is `inf`. Do not clip.

### Hints

<details>
<summary>Hint 1</summary>

Build `stoi` from `itos`, collect the row and column indices of every pair into two lists, then index `probs` once with both lists.

</details>

<details>
<summary>Hint 2</summary>

Mean of the negative logs is `-np.log(p).mean()`.

</details>

## Theory

### The simple version

Think of a student sitting a quiz where every answer is a probability. Full marks go to the student who put almost all their weight on the right answer each time. NLL is the average penalty, and the penalty for being confidently wrong is enormous.

### The formula

$$
\text{NLL} = -\frac{1}{T}\sum_{t=1}^{T} \ln P(c_{t+1} \mid c_t)
$$

where $T$ is the total number of pairs. A uniform model over $V$ symbols has $P = 1/V$ everywhere, so $\text{NLL} = \ln V$. The exponential of NLL is the perplexity, the effective number of equally likely choices.

### How this is done in practice

Every deep learning framework ships this as cross-entropy on the true next token, for example `torch.nn.functional.cross_entropy`, so training a neural language model is literally minimizing this number. Reported numbers are often in bits (divide by `ln 2`) or exponentiated into perplexity, and they are only comparable between models that use the same tokenizer.

## Explanation

The function converts every pair to two indices, looks up all probabilities in one fancy-indexing step and averages their negative logs. The uniform baseline falls out of the formula without any special case, which makes it a useful sanity test: if your model scores worse than `ln V` something is broken. Test words are scored with the same boundary wrapping used when counting, so word starts and ends are part of the score.
