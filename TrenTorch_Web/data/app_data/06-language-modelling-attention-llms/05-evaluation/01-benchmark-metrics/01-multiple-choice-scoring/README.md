---
name: lm-multiple-choice-scoring
title: Multiple-Choice Likelihood Scoring
tags: [evaluation, benchmarks, mmlu]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Many benchmarks ask a model to pick one of several answers. A language model does not output "B"; it assigns probabilities to text. The usual trick is to score each candidate continuation by the log-probability the model gives it and choose the highest. That immediately raises a fairness problem: a longer answer has more tokens and each token multiplies in another probability below one, so long answers are penalized for length alone. Normalizing by length removes most of that bias but introduces a different preference, so the choice of normalization is part of the benchmark definition and can change which model wins.

### From theory to code

Implement `choice_scores`, `pick_choice` and `multiple_choice_accuracy`.

### Constraints

- `logprobs` is a 1-D array holding the **summed** token log-probability of each candidate. `lengths` holds each candidate's length (tokens or characters) as positive numbers.
- `choice_scores(logprobs, lengths, mode)` returns `logprobs` for `mode='sum'` and `logprobs / lengths` for `mode='mean'`. Any other mode raises `ValueError`.
- `pick_choice(logprobs, lengths, mode)` returns the index of the highest score. Ties go to the lowest index (`np.argmax` behaviour).
- `multiple_choice_accuracy(all_logprobs, all_lengths, labels, mode)` takes lists with one entry per question and returns the fraction picked correctly as a float.

### Hints

<details>
<summary>Hint 1</summary>

`np.argmax` already breaks ties toward the first index.

</details>

<details>
<summary>Hint 2</summary>

Compute the scores once per question and compare the argmax with the label.

</details>

## Theory

### The simple version

Asked "what is the capital of France?" a model that writes "Paris" and another that writes "The capital city is Paris" are both right, but the second answer has far more words to be unlucky on. Dividing by length asks "how plausible was each word on average" instead of "how plausible was the whole sentence".

### The formula

$$
\text{score}_i^{\text{sum}} = \sum_{t} \ln p(w_{i,t} \mid \text{prompt}, w_{i,<t}), \qquad
\text{score}_i^{\text{mean}} = \frac{1}{\ell_i}\,\text{score}_i^{\text{sum}}
$$

The prediction is $\arg\max_i \text{score}_i$. Accuracy is the fraction of questions where the prediction equals the labelled answer.

### How this is done in practice

Evaluation harnesses such as EleutherAI's `lm-evaluation-harness` report both `acc` (sum) and `acc_norm` (length-normalized, by characters or tokens) for exactly this reason. Newer benchmarks instead show the options in the prompt and ask the model to generate a letter, which sidesteps likelihood scoring but depends on instruction-following.

## Explanation

The three functions layer cleanly: scores per candidate, the best index per question, and an average over questions. Raising `ValueError` for unknown modes avoids silently reporting a metric nobody asked for. The test cases are built so that the two modes disagree on the same input, which is the point of the exercise.
