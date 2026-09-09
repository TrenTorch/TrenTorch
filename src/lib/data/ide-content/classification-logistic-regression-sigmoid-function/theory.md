# Theory: Sigmoid

## What

Sigmoid maps any real number onto the open interval (0, 1):

```
sigmoid(x) = 1 / (1 + exp(-x))
```

Large positive `x` pushes the output toward 1, large negative `x` toward 0, and `x = 0` lands exactly on 0.5. Because the output always sits in (0, 1), it's the natural choice whenever you need something that reads as a probability.

## Why logistic regression needs it

Linear regression's raw output (`wx + b`) is unbounded -- it can be any real number, which is fine for predicting a price but meaningless as "the probability this email is spam." Sigmoid is the piece that turns an unbounded linear score into a bounded probability, which is what makes the loss function (binary cross-entropy, a later question in this track) well-defined.

## How it maps onto real PyTorch

`torch.sigmoid(x)` (and the equivalent `torch.nn.functional.sigmoid`) computes precisely this. `nn.Sigmoid()` is the `nn.Module` wrapper around the same function, used either as a classifier's final layer or, historically, as a hidden-layer activation before ReLU became the default (see the next question in this curriculum for why that changed).

## When to use it (and when not to)

Use sigmoid at the output layer of a binary classifier, where "probability of the positive class" is exactly what you want. Avoid it as a _hidden_-layer activation in a deep network: its gradient is at most 0.25 and shrinks toward 0 the further `x` is from 0, so stacking many sigmoid layers causes the vanishing-gradient problem -- gradients shrink to nothing by the time they backpropagate to the first layer.

## Pros and cons

- **Pros:** output has a clean probabilistic interpretation; smooth and differentiable everywhere.
- **Cons:** saturates for large |x| (the curve goes nearly flat, so gradients vanish there); output isn't zero-centered, which slows convergence in deep stacks; more expensive to compute than ReLU (an `exp` call vs. a comparison).

## At scale

A single sigmoid call is cheap, but "cheap per call, called constantly" is still a cost: in a deep network with millions of activations per forward pass, the exponential in sigmoid is measurably slower than ReLU's `max(0, x)`. That's one of several reasons modern architectures reserve sigmoid for output layers and gates (like an LSTM's forget gate) rather than using it throughout the network.
