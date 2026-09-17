---
name: variational-circuits-the-ansatz-parameter-shift-vqc
title: 'THE ANSATZ'
tags: [quantum-computing, quantum-machine-learning, optimization, physics]
difficulty: Advanced
---

## Statement

**Difficulty:** Hard
**Topic:** Variational Quantum Circuits, Parameter-Shift Gradients, Quantum Machine Learning

---

### Story

You're an intern at QuantEdge Capital, a fund experimenting with early quantum hardware for
trading-signal classification. Their prototype device only reliably runs a handful of qubits,
so the research team settled on a **hardware-efficient variational quantum circuit**: encode
each market feature as a single-qubit rotation, entangle the qubits, apply a small number of
trainable rotation layers, and read out one qubit's expectation value as the predicted signal.

Real quantum hardware is expensive lab time, so before touching the device you're asked to
build the **classical simulator and trainer** first: simulate the circuit's exact quantum
state, compute gradients using the *parameter-shift rule* (the standard way to differentiate
a quantum circuit — you cannot backpropagate through real hardware, but this identity lets you
get an exact gradient using only two extra circuit evaluations per parameter), and train the
circuit's parameters with gradient descent.

---

### The circuit

You work with `n` qubits (`1 ≤ n ≤ 4`), state space dimension `2^n`, initialized to
`|0...0⟩`. All gates used are **real-valued**, so the state vector's amplitudes stay real
throughout — no complex arithmetic is ever required (this is exactly the "RealAmplitudes"
family of ansätze used in real near-term quantum ML). Qubits are indexed `0 .. n-1`.

Two gates are used:

```
RY(θ) = [[cos(θ/2), -sin(θ/2)],
         [sin(θ/2),  cos(θ/2)]]     (acts on one qubit)

CNOT(control, target): if control qubit is |1⟩, flip target qubit; otherwise do nothing.
```

**Fixed circuit structure**, given a feature vector `x ∈ ℝ^n` and trainable parameters
`θ`, organized as `L` layers of `n` angles each (`θ_{l,i}`, `l = 0..L-1`, `i = 0..n-1`):

1. **Encoding layer:** for `i = 0 .. n-1`, apply `RY(x_i)` to qubit `i`.
2. For each layer `l = 0 .. L-1`:
   a. **Entangling chain:** for `i = 0 .. n-2`, apply `CNOT(control=i, target=i+1)`, in
      increasing order of `i`.
   b. **Rotation layer:** for `i = 0 .. n-1`, apply `RY(θ_{l,i})` to qubit `i`.

(If `n = 1` the entangling chain is empty — there is nothing to entangle with one qubit.)

**Measurement / model output:** the prediction is the exact expectation value of the Pauli-Z
operator on qubit `0`:

```
p(x, θ) = ⟨ψ| Z⊗I⊗...⊗I |ψ⟩ = P(qubit 0 = |0⟩) - P(qubit 0 = |1⟩)
```

where `|ψ⟩` is the final state after the full circuit above. `p(x, θ) ∈ [-1, 1]` always.

---

### Training

You're given `n_train` labeled examples `(x_i, y_i)`, `y_i ∈ ℝ` (targets are **not**
restricted to `[-1,1]` even though the model's output is — this is an ordinary regression
setup with mean squared error loss):

```
Loss(θ) = (1 / n_train) * Σ_i ( p(x_i, θ) - y_i )^2
```

For any parameter `θ_{l,i}` that enters the circuit only through an `RY` rotation, the
**exact** gradient of the output (no approximation, no finite-difference error) is given by
the parameter-shift rule:

```
∂p(x,θ) / ∂θ_{l,i} = [ p(x, θ + (π/2)·e_{l,i}) - p(x, θ - (π/2)·e_{l,i}) ] / 2
```

where `e_{l,i}` is the unit vector shifting only `θ_{l,i}`. (This is a standard identity for
Pauli-rotation gates — you may use it directly without re-deriving it.) By the chain rule:

```
∂Loss/∂θ_{l,i} = (2 / n_train) * Σ_i ( p(x_i,θ) - y_i ) * ∂p(x_i,θ)/∂θ_{l,i}
```

Starting from a given initial `θ_init`, run exactly `T` steps of **full-batch gradient
descent** with fixed learning rate `η`:

```
θ ← θ - η · ∇Loss(θ)
```

(Gradient computed fresh from the full training set at every step, using the parameter-shift
rule above for every one of the `L·n` parameters — that's `2·L·n` extra circuit simulations
per training step.) After `T` steps, use the final `θ` to predict on the query points.

---

### Input Format

```
n_train n L
x_1,1 x_1,2 ... x_1,n y_1
x_2,1 x_2,2 ... x_2,n y_2
...
x_n_train,1 ... x_n_train,n y_n_train
eta T
theta_0,0 theta_0,1 ... theta_0,n-1 theta_1,0 ... theta_L-1,n-1
m
q_1,1 q_1,2 ... q_1,n
...
q_m,1 q_m,2 ... q_m,n
```

- `theta_init` is given **flattened**, layer-major then qubit-index-minor (i.e. all of layer
  `0`'s `n` angles, then all of layer `1`'s, etc.) — exactly `L·n` numbers on one line.
- `eta > 0`, `T ≥ 0` (an integer number of gradient steps; `T = 0` means output predictions
  using `theta_init` unchanged).

### Output Format

Print `m` lines: the predicted `p(q, θ_final)` for each query point, with at least 6 digits
after the decimal point.

**Judging:** accepted if within `1e-4` absolute error of the reference solution (relative
tolerance is not used here, since all valid outputs lie in `[-1, 1]`).

---

### Constraints

- `1 ≤ n_train ≤ 50`
- `1 ≤ n ≤ 4` (qubits)
- `1 ≤ L ≤ 4` (variational layers)
- `1 ≤ m ≤ 50`
- `0 < eta ≤ 2`
- `0 ≤ T ≤ 20`
- All feature values, targets, and initial angles satisfy `|value| ≤ 10` (radians for angles),
  given with up to 6 decimal digits.
- Time limit: 4 seconds. Memory limit: 256 MB.

---

### Example 1

**Input**
```
2 2 1
0.5 -0.3 1.0
1.0 0.2 -1.0
0.5 3
0.1 -0.1
2
0.4 0.4
-0.2 0.6
```

**Output**
```
0.571864
0.794600
```

**Explanation:** `n_train=2` examples, `n=2` qubits, `L=1` layer, learning rate `0.5`, `T=3`
gradient descent steps from `θ_init = [0.1, -0.1]`. After simulating the encode→entangle→
rotate circuit, computing the parameter-shift gradient of the MSE loss over both training
points at every step, and applying `3` updates, the trained parameters converge to
approximately `θ ≈ [0.7482, -0.1000]`. Evaluating the trained circuit at the two query points
gives `0.571864` and `0.794600`.

---

### Example 2

**Input**
```
3 2 2
0.3 0.7 1.0
-0.5 0.1 -1.0
0.9 -0.4 0.5
0.3 2
0.2 0.0 -0.1 0.3
2
0.0 0.0
0.5 -0.5
```

**Output**
```
0.861363
0.967439
```

**Explanation:** Now `n=2` qubits but `L=2` layers (`4` trainable parameters total, given
flattened as `[θ_{0,0}, θ_{0,1}, θ_{1,0}, θ_{1,1}] = [0.2, 0.0, -0.1, 0.3]`), `3` training
examples, learning rate `0.3`, `T=2` steps. Each layer applies its own entangling chain before
its rotation — so the circuit here entangles the qubits **twice** before measurement. The
trained circuit evaluated at the two query points gives `0.861363` and `0.967439`.

---

### Hidden Test Categories

1. **`n = 4` maximum qubits** — full `16`-dimensional state vector simulation, checking the
   gate-application logic generalizes beyond 2 qubits and the CNOT chain correctly touches
   every adjacent pair.
2. **`L = 4` maximum layers** — `4n` trainable parameters, `8n` extra circuit evaluations per
   gradient step; checks parameter-shift bookkeeping doesn't mix up which `θ_{l,i}` is being
   shifted.
3. **`T = 0`** — no training at all; output must equal a direct forward pass through
   `theta_init`, catching implementations that always perform at least one update.
4. **`n = 1` (no entangling chain)** — checks the empty-loop edge case doesn't crash or
   silently insert a phantom CNOT.
5. **Targets outside `[-1, 1]`** — large-residual regression targets, checking gradient signs
   and magnitudes are correct even when the model can never perfectly fit the data.
6. **Large `T` (up to 20) with larger `n_train` (up to 50)** — pure computational stress test
   requiring an efficient state-vector simulation (not, say, building the full `2^n × 2^n`
   unitary matrix explicitly for each gate, which would be needlessly slow and error-prone at
   `n=4`).
7. **Parameter-shift sign check** — small circuits engineered so that a `+π/2`/`-π/2` swap in
   the shift rule produces a detectably different (wrong-signed) gradient and thus a wrong
   trained model.
8. **`eta` large enough to overshoot** — checks that gradient descent is implemented exactly
   as specified (no learning-rate decay, no momentum, no clipping) even when this makes the
   loss temporarily increase.

## Theory

### The simple version

A normal neural network's gradient comes from backpropagation: you can inspect every
intermediate value and apply the chain rule directly, because the whole computation happens
inside classical memory you can read from. A quantum circuit running on real hardware offers
no such thing — you can prepare a circuit, run it, and measure an expectation value, but you
cannot "look inside" the quantum state mid-circuit without collapsing it. Differentiating a
quantum circuit therefore needs a completely different trick: run the *same* circuit twice
more, with one parameter nudged by a fixed amount in each direction, and combine the two
measurements algebraically into an *exact* derivative. That's the parameter-shift rule — not
an approximation like a classical finite-difference gradient (which only converges to the true
gradient as the step size shrinks to zero), but an exact identity for this specific gate family.

### The formula

The circuit is a sequence of single-qubit `RY` rotations and two-qubit `CNOT` gates. `RY(θ)`
is generated by the Pauli-Y operator, and for any observable built from Pauli operators (like
the Pauli-Z measurement here), a rotation gate's exact derivative satisfies:

$$
\frac{\partial}{\partial \theta} \langle \psi(\theta) | \hat{O} | \psi(\theta) \rangle
= \frac{1}{2}\Big[ \langle \psi(\theta + \tfrac{\pi}{2}) | \hat{O} | \psi(\theta + \tfrac{\pi}{2}) \rangle
- \langle \psi(\theta - \tfrac{\pi}{2}) | \hat{O} | \psi(\theta - \tfrac{\pi}{2}) \rangle \Big]
$$

This holds *regardless of what the rest of the circuit does* around that one gate (the
entangling `CNOT`s, the other rotations) — the shift is applied to exactly one parameter,
everything else stays fixed, and the two resulting expectation values (two full circuit
simulations, or two real hardware runs) give the exact partial derivative with respect to
that one angle. Training then follows the same structure as every other model in this
curriculum: compute `Loss(θ)`, compute `∇Loss(θ)` (here, one parameter-shift pair per
parameter instead of one autodiff backward pass), and step downhill with a fixed learning
rate, exactly like `Full Linear Regression Training Loop` does for a classical linear model.

### How real quantum ML frameworks actually implement this

Frameworks built for training circuits on real quantum hardware or noisy simulators — PennyLane
and Qiskit's machine learning modules chief among them — implement exactly this parameter-shift
rule as their default differentiation strategy for rotation gates, specifically *because*
backpropagation (which needs access to every intermediate state) isn't physically realizable on
real hardware, only in a classical simulator like the one this question builds by hand. A
classical simulator (what you're building here) *could* use ordinary backprop through the
state-vector math instead, since every intermediate amplitude is available in memory — but
using parameter-shift even in simulation is the standard choice, since it's the same code path
that will later run unmodified against real hardware, with no separate "simulator gradient"
and "hardware gradient" implementation to keep in sync.

## Explanation

`circuit_output` builds the `2^n`-dimensional real state vector as an `n`-axis tensor of shape
`(2,) * n`, applies the encoding `RY` rotations, then for each of the `L` layers applies the
`CNOT` entangling chain followed by that layer's `RY` rotations — each gate implemented as a
local operation on one or two axes of the tensor (moving the relevant qubit axis to the front,
mixing the two components with the gate's `2x2` matrix or swapping them for `CNOT`'s
control-`1` half, then moving the axis back), never materializing a full `2^n x 2^n` unitary
matrix. The final measurement sums squared amplitudes over qubit 0's two halves and returns
their difference. `train_and_predict` reshapes `theta_init` into `(L, n)`, then for each of
`T` steps evaluates the current predictions and residuals over the full training set, computes
every parameter's gradient via two parameter-shifted forward passes per training example
(the `2·L·n` extra simulations the problem describes), and takes one gradient-descent step.
After training, it reuses `circuit_output` directly on every query row to produce the final
predictions.
