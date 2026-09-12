---
name: math-conditional-probability
title: Conditional probability from a joint distribution
tags: [probability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

"What's the chance it rains AND traffic is bad" is one question. "Given that it's raining, what's the chance traffic is bad" is a different, more useful one, it's the question you'd actually ask before deciding whether to leave early. The first is a joint probability, both things happening together. The second, conditional probability, restricts your attention to only the world where the condition holds, then asks about the other variable within that restricted world.

Turning a joint distribution over two variables into marginals (one variable alone) and conditionals (one variable, given a specific value of the other) is the basic manipulation every probabilistic model relies on, Naive Bayes (Classical ML) is built by combining conditional probabilities exactly like these.

### From theory to code

Theory represents a joint distribution over two discrete variables as a 2D array (`joint[i, j] = P(X=i, Y=j)`), gets a marginal by summing out the other variable, and gets a conditional by slicing to a fixed value of one variable and renormalizing so the slice becomes a valid probability distribution again.

Implement `marginal_x(joint)`, `marginal_y(joint)` and `conditional_x_given_y(joint, y_index)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `joint` is a 2D array summing to `1.0` overall (a valid joint probability table).
- Every returned distribution (marginal or conditional) must itself sum to `1.0`.
- `conditional_x_given_y` must renormalize, not just return the raw column slice.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Summing a 2D array along `axis=1` collapses columns (summing out the second index); `axis=0` collapses rows (summing out the first).

</details>

<details>
<summary>Hint 2</summary>

A single column of `joint` doesn't sum to 1 on its own, dividing by its own sum is what turns it into a valid conditional distribution.

</details>

## Theory

### The simple version

Imagine a weather log tracking two things every day: whether it rained, and whether traffic was bad. A joint probability answers "what fraction of ALL days had both rain and bad traffic." A marginal answers "what fraction of ALL days had rain, regardless of traffic," found by adding up every row of the log that mentions rain, no matter what the traffic column says. A conditional answers a narrower question: "of the days it rained, what fraction ALSO had bad traffic," found by looking ONLY at the rainy days and asking about traffic within that smaller group.

### The formula

For a joint distribution over two discrete variables, `joint[i, j] = P(X=i, Y=j)`, a marginal sums out the other variable:

```text
P(X=i) = sum_j(P(X=i, Y=j))
P(Y=j) = sum_i(P(X=i, Y=j))
```

A conditional distribution restricts to a fixed value of one variable and renormalizes:

```text
P(X=i | Y=y) = P(X=i, Y=y) / P(Y=y) = P(X=i, Y=y) / sum_i(P(X=i, Y=y))
```

Dividing by `P(Y=y)` (the column's own sum) is what turns an unnormalized slice of the joint table back into a valid probability distribution over `X` alone, one that sums to `1` on its own, exactly the requirement any probability distribution must satisfy.

### How PyTorch actually implements this

Naive Bayes (`02-naive-bayes-bernoulli`/`03-gaussian-naive-bayes`, in Classical ML) is built directly on this manipulation: it estimates `P(feature | class)` for every feature, exactly a conditional distribution like this question computes, then combines them (via the "naive" independence assumption) to answer `P(class | all features)` using Bayes' theorem, the next question in this track. More broadly, every categorical distribution `torch.distributions.Categorical` represents, and every softmax output a classifier produces, IS a discrete probability distribution over classes, and computing "the probability of class A given that the input looked like X" is the same marginal/conditional manipulation this question performs by hand on a small, fully-enumerated table.

## Explanation

`marginal_x` sums `joint` along `axis=1` (collapsing every column, summing out `Y`), leaving one entry per value of `X`.

`marginal_y` sums along `axis=0` (collapsing every row, summing out `X`), leaving one entry per value of `Y`.

`conditional_x_given_y` slices out column `y_index` (the joint probabilities for that specific value of `Y`, across every value of `X`) and divides by that column's own sum, renormalizing it into a valid distribution over `X` alone.
