---
name: rl-alignment-tabular-q-learning
title: Tabular Q-Learning
tags: [reinforcement-learning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-value-iteration-mdp` found the exact optimal values — but it needed the _entire_ MDP handed to it up front (`P` and `R`, in full). Q-learning solves the more realistic problem: an agent that can only ever take one action at a time and observe what happens, with no idea what the transition probabilities or reward function actually are. It has to learn the same optimal values purely from lived experience.

### From theory to code

Implement `epsilon_greedy_action` (balancing exploring new actions against exploiting known-good ones), `q_learning_update` (the core temporal-difference learning rule), and `train_q_learning`, which runs the full learning loop against an MDP the agent only ever _samples_ from, never inspects directly.

### Constraints

- `epsilon_greedy_action(Q, state, epsilon, rng)` returns a uniformly random action with probability `epsilon`, otherwise `argmax(Q[state])`.
- `q_learning_update(Q, state, action, reward, next_state, alpha, gamma, done)` updates `Q[state, action] += alpha * (target - Q[state, action])`, where `target = reward` if `done`, else `reward + gamma * max(Q[next_state])`.
- `train_q_learning` never reads `P`/`R` to plan — it only ever samples one transition (`next_state ~ P[state, action]`, `reward = R[state, action, next_state]`) at a time, exactly as a real environment interaction would work.
- After enough episodes, `train_q_learning`'s learned `Q` should approximate the same optimal values `value_iteration` finds exactly on the identical MDP.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The Q-learning update's `target` is exactly the right-hand side of one Bellman backup (`01-value-iteration-mdp`'s `bellman_backup`), but evaluated using a single _sampled_ transition instead of the full expectation over all possible next states — that's the whole difference between model-based and model-free learning.

</details>

<details>
<summary>Hint 2</summary>

`train_q_learning`'s episode loop is: pick a random start state, then repeatedly (pick action via epsilon-greedy, sample the next state with `rng.choice(num_states, p=P[state, action])`, look up the reward, run `q_learning_update`, move to the next state) until landing in a terminal state.

</details>

## Theory

### The simple version

Imagine learning to navigate a new city with no map at all — every time you take a turn, you find out where it led and whether it was a good choice (a reward), and you gradually build up your own personal notes ("turning left at this corner tends to lead somewhere good") purely from having actually walked those routes. You occasionally deliberately take an unfamiliar turn just to see what's there (exploration), rather than only ever following your current best guess (exploitation) — otherwise you'd never discover a better route you haven't tried yet. Q-learning is exactly this process, formalized: a table of "how good is this action from this state" estimates, updated a little bit every time a real experience disagrees with the current estimate.

### The formula

```text
epsilon_greedy_action(Q, s, epsilon):
    random action with probability epsilon        (explore)
    argmax(Q[s]) with probability 1 - epsilon      (exploit)

q_learning_update (the temporal-difference rule):
    target = reward                                     if done
           = reward + gamma * max_a' Q[next_state, a']   otherwise
    Q[state, action] += alpha * (target - Q[state, action])
```

`alpha` (the learning rate) controls how much each single experience nudges the current estimate — too high and the estimates bounce around noisily forever; too low and learning is painfully slow. Given enough episodes (and enough exploration to actually visit every state-action pair many times), tabular Q-learning is provably guaranteed to converge to the exact same optimal `Q`-values that `01-value-iteration-mdp`'s model-based approach computes directly.

### How PyTorch actually implements this

Context only, untested by your submission: tabular Q-learning (Watkins, 1989) only scales to MDPs small enough to store a full `Q`-table for — real-world RL and RLHF pipelines (this section's `02-post-training-alignment` track) instead train a neural network to _approximate_ the `Q`-function (or a policy directly), which is exactly what techniques like PPO build on: the same underlying "improve your estimate from real interaction" idea, just with a differentiable function approximator standing in for the table.

## Explanation

`epsilon_greedy_action` implements the standard explore/exploit tradeoff directly: a coin flip against `epsilon` decides whether to try a uniformly random action or trust the current best-known one.

`q_learning_update` computes the temporal-difference target — the reward just observed, plus (unless the episode ended) a bootstrap off the _current_ estimate of the best achievable value from `next_state` — and nudges `Q[state, action]` toward that target by a fraction `alpha` of the gap between them.

`train_q_learning` runs the full model-free learning loop: for each episode, start at a random state and repeatedly act, sample a real transition from the environment's (hidden, only-ever-sampled) dynamics, and apply `q_learning_update`, until a terminal state ends the episode. This exercise's `tests.py` verifies the learned `Q`-table converges close to `01-value-iteration-mdp`'s exact `value_iteration` output on the identical MDP — a genuine independent oracle, since Q-learning never sees `P`/`R` directly and has to rediscover the same optimal values purely from sampled experience — and that the learned _greedy policy_ matches the true optimal policy exactly, not just the values approximately.
