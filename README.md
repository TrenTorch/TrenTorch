<div align="center">

<img src=".github/assets/trentorch-logo.png" width="120" height="120" alt="TrenTorch logo" />

# TrenTorch

[![CI](https://github.com/TrenTorch/TrenTorch/actions/workflows/validate.yml/badge.svg?branch=TrenTorch-Dev)](https://github.com/TrenTorch/TrenTorch/actions/workflows/validate.yml)
[![Contributors](https://img.shields.io/badge/contributors-7-orange.svg)](#team-engineers)
[![CodeFactor](https://www.codefactor.io/repository/github/trentorch/trentorch/badge)](https://www.codefactor.io/repository/github/trentorch/trentorch)
[![Python](https://img.shields.io/badge/python-3.10+-3776ab?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/license-PolyForm--Noncommercial--1.0.0-blue.svg)](LICENSE)

**Learn ML by building it: a from-scratch machine learning framework in NumPy, and hundreds of coding questions that run in your browser.**

[Try it in the browser](https://trentorch.com) · [Run it locally](#run-it-locally) · [The CLI curriculum](#the-cli-curriculum-20-modules) · [Contributing](TrenTorch_CLI/docs/CONTRIBUTING.md)

</div>

---

> [!NOTE]
> The CLI curriculum is our implementation of [TinyTorch](https://mlsysbook.ai/tinytorch) (Harvard CS249r), rebuilt and extended in our own style. The browser version is our own, built independently.

---

## Two ways to learn

TrenTorch is one repository with two products that cover the same ground.

| | [TrenTorch Web](https://trentorch.com) | TrenTorch CLI |
|---|---|---|
| **Where** | Your browser, nothing to install | Your terminal and Jupyter |
| **What** | 350+ coding questions in 12 topic areas, from linear algebra to inference and distributed training | 20 modules that build a framework, from tensors to a capstone |
| **How it runs** | Python 3.12 in the browser (Pyodide). Your code runs on your machine and is graded instantly | A local `tren` command, notebooks, and a test suite per module |
| **Progress** | Saved to your account (GitHub, Google, or email sign-in) | Saved locally under `user_data/` |
| **Code** | [`TrenTorch_Web/`](TrenTorch_Web) (SvelteKit) | [`TrenTorch_CLI/`](TrenTorch_CLI) (Python) |

<p align="center">
  <img src=".github/assets/screenshot-questions.png" width="49%" alt="The TrenTorch questions page: a list of tracks with question counts and a progress bar" />
  <img src=".github/assets/screenshot-ide.png" width="49%" alt="The TrenTorch in-browser editor: problem statement on the left, Python editor and test results on the right" />
</p>

---

## Run it locally

### CLI

```bash
# macOS / Linux
git clone https://github.com/TrenTorch/TrenTorch.git
cd TrenTorch/TrenTorch_CLI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
tren setup
tren
```

```powershell
# Windows (PowerShell)
git clone https://github.com/TrenTorch/TrenTorch.git
cd TrenTorch\TrenTorch_CLI
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
tren setup
tren
```

`tren setup` adds `tren` to your PATH. After that, every terminal just needs `tren`, no activating first. Run `tren module start 01` to begin, and see the [command reference](TrenTorch_CLI/docs/command-reference.md) for everything else (`tren tui`, `tren serve`, `tren milestone`, `tren benchmark`).

### Web

```bash
cd TrenTorch_Web
npm install
npm run dev
```

Sign-in uses Supabase. Copy `.env.example` to `.env` and fill in your own project keys to use it locally.

| Command | What it does |
|---|---|
| `npm run check` | Type check |
| `npm run lint` | Prettier and ESLint |
| `npm run test` | Unit tests (Vitest) |
| `npm run test:pyodide` | Runs every question's reference solution and tests in a real Pyodide |
| `npm run build` | Production build (fully prerendered) |

---

## Why build it yourself

Most people learn ML frameworks by importing them. We wanted to know how they work, so we built one.

- **Small enough to read**: every operation traces back to raw NumPy
- **Real enough to matter**: the same architecture production frameworks use
- **No black boxes**: no `import torch` anywhere in the curriculum

```python
# Most courses:
import torch
model.fit(X, y)  # everything happens somewhere else

# TrenTorch:
# You implement every component
# You measure memory usage
# You optimize performance
```

You end up knowing what `loss.backward()` does because you wrote it, and memory, compute and scaling stop being abstractions.

---

## The web curriculum

The browser version is organized into 12 topic areas, each split into tracks. Every question has a problem statement, a theory section, a starter file, tests, and a reference solution.

| Area | Tracks |
|---|---|
| Math and statistics | Linear algebra, calculus, probability, information theory, data preprocessing, exploratory analysis, statistical inference |
| Classical ML | Linear regression, classification, decision trees, regularized models, ensembles, SVMs, instance-based and probabilistic models, unsupervised learning, evaluation, tabular foundation models |
| Deep learning core | Tensors, activations, losses, autograd |
| Training | Optimizers, layers, the training loop, regularization, why deep networks work |
| Sequence modeling | Tokenization, embeddings, recurrent networks, attention |
| Transformers and LLMs | The transformer block, modern architectures, language model assembly, LLM engineering |
| Inference | Attention mechanisms, KV cache and decoding, quantization, batching and serving metrics |
| Vision | Convolutions, pooling, CNN architecture and history, modern CNN concepts, vision transformers |
| Systems performance | Profiling, quantization, mixed-precision training, compression, acceleration, kernels |
| Distributed systems | Memoization, parallelism |
| RL and alignment | Reinforcement learning, post-training alignment, fine-tuning, benchmarking and a capstone |
| Production ML | Experiment tracking and versioning, deployment and serving, monitoring and drift |

A **Problem of the Day** features one new question every day.

---

## The CLI curriculum: 20 modules

| Part | Modules | What you build |
|---|---|---|
| I. Foundations | 01-08 | Tensors, activations, layers, losses, dataloader, autograd, optimizers, training |
| II. Vision | 09 | Conv2d, CNNs for image classification |
| III. Language | 10-13 | Tokenization, embeddings, attention, transformers |
| IV. Optimization | 14-20 | Profiling, quantization, compression, acceleration, memoization, benchmarking, capstone |

### Historical milestones

As you progress, you unlock recreations of landmark ML results, run on your own framework:

| Year | Milestone | What you reproduce |
|---|---|---|
| 1958 | Perceptron | Binary classification with gradient descent |
| 1969 | XOR Crisis | Multi-layer networks solving non-linear problems |
| 1986 | Backpropagation | Multi-layer network training |
| 1998 | CNN Revolution | Image classification with convolutions |
| 2017 | Transformer Era | Language generation with self-attention |
| 2018+ | MLPerf | Production-grade optimization |

---

## Repository structure

```text
TrenTorch/
├── TrenTorch_CLI/                 # The `tren` CLI and the framework curriculum
│   ├── data/
│   │   ├── src/                       # Curriculum source (edit here), 01_tensor to 20_capstone
│   │   ├── modules/                   # Generated notebooks (student-facing, stubs only)
│   │   ├── solutions/                 # Reference implementations (maintainer and CI only)
│   │   ├── datasets/                  # Small training datasets
│   │   ├── milestones/                # Historical ML recreations
│   │   └── trentorch/                 # Generated package you import from
│   ├── platforms/
│   │   ├── cli/                       # The `tren` CLI
│   │   │   ├── core/                      # Config, console, theme, runtime
│   │   │   ├── cli_platform/              # Setup, system, package and dev commands
│   │   │   ├── processes/                 # Module workflow, milestone, benchmark, olympics, convert
│   │   │   ├── tui/                       # Terminal dashboard
│   │   │   ├── server/, companion_ui/     # Local companion web UI
│   │   │   └── tests/
│   │   └── dev_tools/                 # Maintainer scripts
│   ├── docs/                          # Command reference, design notes, contributing guide
│   ├── user_data/                     # Your progress and benchmarks (not committed)
│   └── tests/                         # Integration, end-to-end and environment tests
│
├── TrenTorch_Web/                 # The browser version (SvelteKit, trentorch.com)
│   ├── platform/                      # Routes, components, assets
│   ├── processes/                     # Question runner, IDE content, POTD, auth, progress
│   ├── data/                          # Curriculum, question content (app_data/), POTD schedule
│   ├── pyodide-check/                 # Runs every question in Pyodide as a repo check
│   ├── e2e/                           # End-to-end and build-output checks
│   ├── supabase/migrations/           # Auth and user-data schema, with RLS policies
│   └── docs/                          # Design specs and plans
│
└── .github/                       # CI, bots and shared assets
```

The CLI workflow: `TrenTorch_CLI/data/src/*.py` becomes `TrenTorch_CLI/data/modules/*.ipynb` (you solve it), and your solutions end up in `TrenTorch_CLI/data/trentorch/*.py`.

---

## Contributing

Issues and pull requests are welcome. Start with the [contributing guide](TrenTorch_CLI/docs/CONTRIBUTING.md): open an issue first, and ask to be assigned before you start on it. CI has to be green and one review from someone other than the author is required to merge. The first-contribution bot greets you on your first PR.

Found a security problem? Do not open a public issue. Read [SECURITY.md](SECURITY.md).

---

## Credit

TrenTorch's CLI is our implementation, built on the curriculum and foundation of [TinyTorch](https://mlsysbook.ai/tinytorch), created by [Prof. Vijay Janapa Reddi](https://vijay.seas.harvard.edu) and the [ML Systems Book](https://mlsysbook.ai) community at Harvard University.

Related educational frameworks worth knowing:
- [tinygrad](https://github.com/tinygrad/tinygrad): George Hotz's minimalist framework
- [micrograd](https://github.com/karpathy/micrograd): Andrej Karpathy's tiny autograd
- [MiniTorch](https://minitorch.github.io/): Cornell's educational framework

---

## Team Engineers

Recomputed nightly from real issue/PR activity via [`.github/workflows/update-contributors.yml`](.github/workflows/update-contributors.yml). Want to show up here? Open an issue, or get a PR merged: the first-contribution bot will say hello on your first PR, and this grid picks you up on the next nightly run after it merges. A closed-without-merging PR doesn't count.

<table width="100%" style="width:100%">
  <tbody>
    <tr>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/maanas1234"><img src="https://avatars.githubusercontent.com/maanas1234?v=4" class="contributor-avatar" width="80px;" alt="maanas1234"/></a>
        <br />
        <b>maanas1234</b>
        <br />
        <sub><strong>Maintainer</strong></sub>
        <br />
        <sub>Catches bugs, builds solutions and ships products</sub>
        <br />
        <sub>Issues: 13 &middot; PRs: 13</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/aadityansha06"><img src="https://avatars.githubusercontent.com/aadityansha06?v=4" class="contributor-avatar" width="80px;" alt="Aadityansha"/></a>
        <br />
        <b>Aadityansha</b>
        <br />
        <sub><strong>Maintainer</strong></sub>
        <br />
        <sub>Reducing CPU stalls, one commit at a time.</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 3</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/Shashank-Tripathi-07"><img src=".github/assets/rocky-avatar.png" class="contributor-avatar" width="80px;" alt="Rocky"/></a>
        <br />
        <b>Rocky</b>
        <br />
        <sub><strong>Principal Maintainer</strong></sub>
        <br />
        <sub>IIT Guwahati, Debugs autograd for fun, ships before sunrise.</sub>
        <br />
        <sub>Issues: 12 &middot; PRs: 154</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/ShivtejG236"><img src="https://avatars.githubusercontent.com/ShivtejG236?v=4" class="contributor-avatar" width="80px;" alt="Shivtej Gaikwad"/></a>
        <br />
        <b>Shivtej Gaikwad</b>
        <br />
        <sub><strong>Maintainer</strong></sub>
        <br />
        <sub>IIT Guwahati. Shows up, ships, moves on to the next thing.</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 4</sub>
      </td>
    </tr>
    <tr>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/JashT14"><img src="https://avatars.githubusercontent.com/JashT14?v=4" class="contributor-avatar" width="80px;" alt="JashT14"/></a>
        <br />
        <b>JashT14</b>
        <br />
        <sub>Spots bugs, corrects them and contributes</sub>
        <br />
        <sub>Issues: 4 &middot; PRs: 3</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/MahekPatel-2403"><img src="https://avatars.githubusercontent.com/MahekPatel-2403?v=4" class="contributor-avatar" width="80px;" alt="MahekPatel-2403"/></a>
        <br />
        <b>MahekPatel-2403</b>
        <br />
        <sub>Spots bugs, corrects them and contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 1</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/pushkarkumarvats"><img src="https://avatars.githubusercontent.com/pushkarkumarvats?v=4" class="contributor-avatar" width="80px;" alt="pushkarkumarvats"/></a>
        <br />
        <b>pushkarkumarvats</b>
        <br />
        <sub>Spots bugs, corrects them and contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 1</sub>
      </td>
    </tr>
  </tbody>
</table>

---

## License

[PolyForm Noncommercial License 1.0.0](LICENSE): free for personal, educational, and noncommercial use. Not licensed for commercial use.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). It applies in issues, pull requests, discussions, and on [trentorch.com](https://trentorch.com).

---

<div align="center">

<b>Build it yourself. Understand it fully.</b>

</div>
