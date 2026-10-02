---
name: math-conditional-probability-bayes
title: "Conditional Probability & Bayes' Theorem"
tags: [probability, foundations]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

**Conditional probability**

"What's the chance it rains AND traffic is bad" is one question. "Given that it's raining, what's the chance traffic is bad" is a different, more useful one, it's the question you'd actually ask before deciding whether to leave early. The first is a joint probability, both things happening together. The second, conditional probability, restricts your attention to only the world where the condition holds, then asks about the other variable within that restricted world.

Turning a joint distribution over two variables into marginals (one variable alone) and conditionals (one variable, given a specific value of the other) is the basic manipulation every probabilistic model relies on, Naive Bayes (Classical ML) is built by combining conditional probabilities exactly like these.

**The chain rule**

**Naming collision, worth stating up front:** this "chain rule" has nothing to do with calculus's chain rule for differentiating composed functions, it's an unrelated rule that happens to share a name, because both describe "a chain of dependent steps multiplied together." Here, the chain rule of probability answers a very practical question: how do you compute the joint probability of several variables when you only know a chain of _conditional_ probabilities, `P(X)`, then `P(Y | X)`, then `P(Z | X, Y)`, and so on? This is exactly how autoregressive language models define the probability of an entire sequence: `P(\text{token}_1) \cdot P(\text{token}_2 \mid \text{token}_1) \cdot P(\text{token}_3 \mid \text{token}_1, \text{token}_2) \cdots`, each token's probability conditioned on every token before it, multiplied together into one number for the whole sequence.

**Bayes' theorem**

A medical test for a rare disease comes back positive. Should you be worried? Your gut says "the test is 99% accurate, so I'm almost certainly sick," but that's the wrong question, it ignores how rare the disease was in the first place. If the disease affects 1 in 100 people, and even a small fraction of HEALTHY people also test positive (a false positive rate), the healthy false-positives can vastly outnumber the sick true-positives in raw counts, even with a 99%-accurate test. The right question is: "of everyone who tests positive, healthy and sick combined, what fraction are actually sick?"

Bayes' theorem is the formula that answers exactly this: it takes a prior belief (how common is the disease, before any test), combines it with how the evidence behaves under each hypothesis (how likely is a positive test if you're sick, vs if you're not), and produces the correct, updated belief (how likely are you sick, given the positive test).

### From theory to code

**Conditional probability**

Theory represents a joint distribution over two discrete variables as a 2D array (`joint[i, j] = P(X=i, Y=j)`), gets a marginal by summing out the other variable, and gets a conditional by slicing to a fixed value of one variable and renormalizing so the slice becomes a valid probability distribution again.

Implement `marginal_x(joint)`, `marginal_y(joint)` and `conditional_x_given_y(joint, y_index)` against that reasoning. The signatures and docstrings are already in the editor.

**The chain rule**

Implement `joint_via_chain_rule(p_x, p_y_given_x, p_z_given_xy)` for the three-variable case, then `chain_rule_general(conditionals)`, generalizing to any number of variables given as a list of conditional-probability factors. The signatures and docstrings are already in the editor.

**Bayes' theorem**

Theory gives the raw formula (`posterior = likelihood * prior / evidence`) and, for the common binary-hypothesis case, shows how to compute the evidence term yourself from the two conditional likelihoods and the prior.

Implement `bayes_theorem(prior, likelihood, evidence)` first, the direct formula, then `posterior_binary(prior_h, likelihood_e_given_h, likelihood_e_given_not_h)`, which computes the evidence term and calls the first function.

### Constraints

**Conditional probability**

- `joint` is a 2D array summing to `1.0` overall (a valid joint probability table).
- Every returned distribution (marginal or conditional) must itself sum to `1.0`.
- `conditional_x_given_y` must renormalize, not just return the raw column slice.

**The chain rule**

- All probability arguments are floats in `[0, 1]`.
- `conditionals` is a non-empty list; its first entry is an unconditional probability, every entry after that is conditioned on all variables before it in the list's order.

**Bayes' theorem**

- All probabilities are plain floats in `[0, 1]`.
- `posterior_binary` must compute the evidence term itself (`P(evidence)`, the total probability of seeing the evidence at all, summed over both the H-true and H-false cases), not take it as a separate argument.
- `posterior_binary` should call `bayes_theorem` rather than reimplementing the same division.

### Hints

**Conditional probability**

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Summing a 2D array along `axis=1` collapses columns (summing out the second index); `axis=0` collapses rows (summing out the first).

</details>

<details>
<summary>Hint 2</summary>

A single column of `joint` doesn't sum to 1 on its own, dividing by its own sum is what turns it into a valid conditional distribution.

</details>

**The chain rule**

<details>
<summary>Hint 1</summary>

`joint_via_chain_rule` is a single multiplication of its three arguments, no conditioning logic to implement, since each argument is already the correctly-conditioned probability.

</details>

<details>
<summary>Hint 2</summary>

`chain_rule_general` is `math.prod(conditionals)`, Python's `math.prod` multiplies every element of an iterable together, which is exactly what an arbitrary-length chain rule needs.

</details>

**Bayes' theorem**

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`bayes_theorem` is one line: multiply, then divide.

</details>

<details>
<summary>Hint 2</summary>

The evidence term is a weighted average: `P(evidence | H) * P(H) + P(evidence | not H) * P(not H)`, and `P(not H) = 1 - P(H)`.

</details>

## Theory

### The simple version

**Conditional probability**

Imagine a weather log tracking two things every day: whether it rained, and whether traffic was bad. A joint probability answers "what fraction of ALL days had both rain and bad traffic." A marginal answers "what fraction of ALL days had rain, regardless of traffic," found by adding up every row of the log that mentions rain, no matter what the traffic column says. A conditional answers a narrower question: "of the days it rained, what fraction ALSO had bad traffic," found by looking ONLY at the rainy days and asking about traffic within that smaller group.

**The chain rule**

Think of drawing colored balls from a bag, one at a time, without replacement, and asking for the probability of a specific sequence of colors. The probability of the _first_ ball being red is unconditional. The probability of the _second_ ball being blue depends on what the first ball was (since it's not replaced, it changed the bag's contents), that's `P(\text{2nd blue} \mid \text{1st red})`. The probability of the whole sequence happening is the product of each step's probability, conditioned on everything drawn before it, you never need the true unconditional probability of "2nd ball blue," only its probability _given_ the specific history that already happened.

**Bayes' theorem**

Before any test, a random person has a small (say, 1%) chance of having a rare disease, that's your prior belief. Now they test positive. How much should that update your belief? It depends on two things you need to know about the test: how often it correctly flags sick people (true positive rate), and how often it WRONGLY flags healthy people (false positive rate). If healthy people vastly outnumber sick people (which they do, when a disease is rare), even a small false-positive rate can produce more false alarms than true detections, so a positive test moves your belief upward, but not nearly as far as "99% accurate" naively suggests.

### The formula

**Conditional probability**

For a joint distribution over two discrete variables, `joint[i, j] = P(X=i, Y=j)`, a marginal sums out the other variable:

$$
P(X=i) = \sum_j P(X=i, Y=j)
$$

$$
P(Y=j) = \sum_i P(X=i, Y=j)
$$

A conditional distribution restricts to a fixed value of one variable and renormalizes:

$$
P(X=i \mid Y=y) = \frac{P(X=i, Y=y)}{P(Y=y)} = \frac{P(X=i, Y=y)}{\sum_i P(X=i, Y=y)}
$$

Dividing by `P(Y=y)` (the column's own sum) is what turns an unnormalized slice of the joint table back into a valid probability distribution over `X` alone, one that sums to `1` on its own, exactly the requirement any probability distribution must satisfy.

**The chain rule**

$$
P(X, Y, Z) = P(X) \cdot P(Y \mid X) \cdot P(Z \mid X, Y)
$$

$$
P(X_1, X_2, \ldots, X_n) = \prod_{i=1}^{n} P\bigl(X_i \mid X_1, \ldots, X_{i-1}\bigr)
$$

- `P(X, Y, Z)`, the joint probability of all three variables taking their specific values simultaneously (same notation as `03-joint-independence`, extended to three variables).
- `P(Y \mid X)`, the conditional probability of `Y`, given that `X`'s value is already known (from `03-joint-independence`).
- `\prod_{i=1}^{n}`, product notation from `00-notation-and-foundations/02-product-notation`; each factor conditions on every variable that came before it in the chosen ordering.

**Bayes' theorem**

$$
P(H \mid \text{evidence}) = \frac{P(\text{evidence} \mid H) \cdot P(H)}{P(\text{evidence})} = \frac{\text{likelihood} \cdot \text{prior}}{\text{evidence}}
$$

- **Prior**, `P(H)`: what you believed before seeing any evidence.
- **Likelihood**, `P(evidence | H)`: how probable the evidence is, assuming the hypothesis is true.
- **Evidence**, `P(evidence)`: the total probability of seeing this evidence at all, under every possible hypothesis.
- **Posterior**, `P(H | evidence)`: your updated belief, after accounting for the evidence.

For a binary hypothesis (`H` true or false), the evidence term expands into two cases:

$$
P(\text{evidence}) = P(\text{evidence} \mid H) \cdot P(H) + P(\text{evidence} \mid \neg H) \cdot P(\neg H)
$$

"The evidence could have come from the world where H is true, or the world where H is false, weighted by how likely each world was to begin with and how likely the evidence is within each."

For the disease example (prior 1%, true positive rate 99%, false positive rate 5%): `P(evidence) = 0.99*0.01 + 0.05*0.99 = 0.0594`, and `P(H | positive test) = 0.99*0.01 / 0.0594 ~= 16.7%`, far below the naive "99% accurate means 99% sick" intuition, exactly the counterintuitive result Bayes' theorem exists to correct for.

### Why any ordering of the variables works

The chain rule holds for _every_ ordering of the variables, not just one, `P(X,Y,Z) = P(Z) \cdot P(Y \mid Z) \cdot P(X \mid Y, Z)` is equally valid. It follows directly from repeatedly applying the definition of conditional probability, `P(A \mid B) = P(A, B) / P(B)`, rearranged to `P(A, B) = P(B) \cdot P(A \mid B)`, one variable at a time. Which ordering is most useful depends entirely on which conditionals are easiest to model or estimate for the problem at hand, autoregressive language models pick the left-to-right token order because it matches how text is generated and read.

### Try it live

**Conditional probability**

<div class="tt-widget" data-widget="math-conditional-probability"></div>

**The chain rule**

<div class="tt-widget" data-widget="math-chain-rule-of-probability"></div>

**Bayes' theorem**

<div class="tt-widget" data-widget="math-bayes-theorem"></div>

### How NumPy/PyTorch actually implements this

**Conditional probability**

Naive Bayes (`02-naive-bayes-bernoulli`/`03-gaussian-naive-bayes`, in Classical ML) is built directly on this manipulation: it estimates `P(feature | class)` for every feature, exactly a conditional distribution like this question computes, then combines them (via the "naive" independence assumption) to answer `P(class | all features)` using Bayes' theorem, the next question in this track. More broadly, every categorical distribution `torch.distributions.Categorical` represents, and every softmax output a classifier produces, IS a discrete probability distribution over classes, and computing "the probability of class A given that the input looked like X" is the same marginal/conditional manipulation this question performs by hand on a small, fully-enumerated table.

**The chain rule**

An autoregressive model (any GPT-style language model) computes exactly `chain_rule_general`'s product at training time, though almost always in log-space (summing `log P(X_i \mid X_{<i})` instead of multiplying raw probabilities) to avoid the underflow the Numerical Computation track's floating-point question covers, `torch.nn.functional.cross_entropy` applied per-token and summed over the sequence _is_ the negative log of this chain-rule product.

**Bayes' theorem**

Naive Bayes classifiers (`02-naive-bayes-bernoulli`, `03-gaussian-naive-bayes`, in Classical ML) are literally this formula, applied at scale: the prior is how common each class is in the training data, the likelihood is `P(features | class)` estimated from the training data, and classification is choosing the class with the highest posterior. More broadly, Bayesian deep learning (a more advanced, less common paradigm than the standard training loops elsewhere in this curriculum) treats a network's weights themselves as a probability distribution updated via Bayes' theorem as training data arrives, rather than a single point estimate optimized by gradient descent, `06-bayesian-optimization` (Evaluation & Model Selection) is the one place in this curriculum's main path where this Bayesian-updating idea shows up directly, choosing which hyperparameters to try next based on a posterior belief about where the best ones are likely to be.

## Explanation

**Conditional probability.** `marginal_x` sums `joint` along `axis=1` (collapsing every column, summing out `Y`), leaving one entry per value of `X`.

`marginal_y` sums along `axis=0` (collapsing every row, summing out `X`), leaving one entry per value of `Y`.

`conditional_x_given_y` slices out column `y_index` (the joint probabilities for that specific value of `Y`, across every value of `X`) and divides by that column's own sum, renormalizing it into a valid distribution over `X` alone.

**The chain rule.** `joint_via_chain_rule` returns `p_x * p_y_given_x * p_z_given_xy`, a direct three-factor multiplication, since each argument is already the correctly-conditioned probability and no further conditioning computation is needed. `chain_rule_general` returns `math.prod(conditionals)`, generalizing the same multiplication to an arbitrary-length list without hand-writing a loop or an explicit accumulator.

**Bayes' theorem.** `bayes_theorem` computes `(likelihood * prior) / evidence` directly, the raw formula.

`posterior_binary` computes the evidence term as a weighted sum over both cases of the hypothesis (`likelihood_e_given_h * prior_h + likelihood_e_given_not_h * (1 - prior_h)`), then calls `bayes_theorem` with that computed evidence, reusing the first function rather than duplicating its division.
