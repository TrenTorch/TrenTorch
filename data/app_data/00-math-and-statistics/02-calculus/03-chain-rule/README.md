---
name: math-chain-rule
title: "Chain rule: composing two functions' derivatives by hand"
tags: [calculus]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A thermostat controls a heater's power, and the heater's power controls the room's temperature. If you want to know "how much does turning the thermostat dial one degree change the room's temperature," you can't answer that from either relationship alone, you need to combine "how much does the dial change the heater's power" with "how much does the heater's power change the temperature." Multiply those two sensitivities together and you get the answer for the whole chain.

That multiplication is the chain rule, and it is not a niche calculus trick, it is the single mechanism behind every gradient this entire curriculum computes. A neural network is nothing but a long chain of composed functions (linear, activation, linear, activation, ...), and "backpropagation" is just this rule, applied once per link in that chain, walking from the output back to the input.

### From theory to code

Theory gives the exact rule for two composed functions: the outer function's derivative, evaluated at the inner function's output, times the inner function's own derivative. Implement a way to compose two functions into one, and a way to compute that combined derivative directly from the pieces (not by composing then finite-differencing).

Implement `compose(f, g)` and `chain_rule_derivative(f_prime, g, g_prime, x)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `compose(f, g)` returns a callable, `h`, such that `h(x) == f(g(x))`.
- `chain_rule_derivative` computes the derivative analytically from `f_prime`, `g` and `g_prime`, it does not call `compose` or approximate with finite differences.
- `f` itself is never needed by `chain_rule_derivative`, only `f_prime`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`compose` is one line: a lambda (or a small nested function) that calls `g` first, then feeds the result into `f`.

</details>

<details>
<summary>Hint 2</summary>

You need `g(x)` before you can evaluate `f_prime` at the right point, `f_prime` is evaluated at the INNER function's output, not at `x` itself.

</details>

## Theory

### The simple version

A thermostat dial controls a heater's power output, and the heater's power output controls the room's temperature. "How much does turning the dial one degree change the room's temperature" isn't answerable from either link alone, you multiply "dial-to-power sensitivity" by "power-to-temperature sensitivity" to get the combined effect. That multiplication of sensitivities, chained end to end, is the chain rule.

### The formula

The chain rule is arguably the single most important rule in this entire curriculum: **every** backward pass this curriculum writes (`03-tanh`'s backward, `linear_regression`'s gradient, the entire Autograd track) is an application of it.

For a composed function `h(x) = f(g(x))` (apply `g` first, then `f` to the result):

```text
h'(x) = f'(g(x)) * g'(x)
```

In words: "the derivative of the outer function, evaluated at the inner function's output, multiplied by the derivative of the inner function." This is exactly the mechanism behind every "backward" this curriculum has implemented so far: `03-tanh`'s `grad_output * (1 - output**2)` is `f'` (the loss's sensitivity to tanh's output, `grad_output`) times `g'` (tanh's own local derivative), chained together. A deep network's full backward pass is just this rule applied over and over, once per layer, from the output back to the input, which is precisely what the Autograd track builds a general engine for.

### How PyTorch actually implements this

`loss.backward()` is, mechanically, nothing but this rule applied automatically, once per operation, along the entire recorded computation graph, in reverse order from the loss back to the leaves. Every differentiable PyTorch operation (`torch.matmul`, `torch.tanh`, even `+`) registers its own local derivative as a small `grad_fn` node during the forward pass; `backward()` walks that graph end to end, multiplying each node's local derivative into the accumulated upstream gradient exactly the way `chain_rule_derivative` multiplies `f_prime(g(x))` by `g_prime(x)` here. This is also precisely why every activation function in `02-deep-learning-core` takes `grad_output` as an argument to its own `_backward`: that parameter IS the accumulated product of every chain-rule link computed so far, upstream of that one operation.

## Explanation

`compose` returns a closure, `lambda x: f(g(x))`, that applies `g` then `f`.

`chain_rule_derivative` computes `g(x)` first (the inner function's value), evaluates `f_prime` there, and multiplies by `g_prime(x)` (the inner function's own derivative at `x`), exactly the formula from Theory.
