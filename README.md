<div align="center">

<img src=".github/assets/trentorch-bolt.svg" width="120" height="120" alt="TrenTorch pulsing bolt mark" />

# TrenTorch

[![Validate](https://github.com/TrenTorch/TrenTorch/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/TrenTorch/TrenTorch/actions/workflows/validate.yml)
[![Contributors](https://img.shields.io/badge/contributors-7-orange.svg)](#team-engineers)
[![CodeFactor](https://www.codefactor.io/repository/github/trentorch/trentorch/badge)](https://www.codefactor.io/repository/github/trentorch/trentorch)
[![Python](https://img.shields.io/badge/python-3.10+-3776ab?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/license-PolyForm--Noncommercial--1.0.0-blue.svg)](LICENSE)
[![Built From Scratch](https://img.shields.io/badge/dependencies-just%20NumPy-D4740C?logo=numpy&logoColor=white)](#what-youll-build)

**Build a real ML framework by hand, from NumPy up through transformers and LLMs.**

[Quick Start](#quick-start) · [Why TrenTorch](#why-trentorch) · [Modules](#20-progressive-modules) · [Milestones](#historical-milestones)

</div>

---

> [!NOTE]
> **This is our implementation of [TinyTorch](https://mlsysbook.ai/tinytorch)** (Harvard CS249r), rebuilt and extended in our own style.

---

## Quick Start

### CLI (local)

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

`tren setup` adds `tren` to your PATH. After that, every terminal just needs `tren`, no activating first.

### Web (browser)

The same curriculum, in the browser: no install, no setup. Live at [trentorch.com](https://trentorch.com), built with [SvelteKit](https://svelte.dev/docs/kit).

```bash
cd TrenTorch_Web
npm install
npm run dev -- --open
```

```bash
npm run check   # types
npm run lint    # prettier + eslint
npm run test    # vitest
npm run build   # production build
```

---

## Why TrenTorch?

Most people learn ML frameworks by importing them. We wanted to know how they actually work, so we built one, then kept going past "good enough."

TinyTorch teaches the fundamentals. TrenTorch takes the same foundation and pushes it further: cleaner internals, a harder curriculum, and an implementation extended past the original spec wherever it made sense.

- **Small enough to read in one sitting**: every operation traces back to raw NumPy
- **Real enough to matter**: the same architecture production frameworks run on
- **Fully ours**: rebuilt and hardened from scratch, not a wrapper around an existing library

No black boxes. No `import torch`. Just the machinery, exposed.

---

## What You'll Build

A complete ML framework, in four stages:

**Vision**: Conv2d, pooling, and CNNs from scratch, evaluated on real benchmarks.

**NLP**: Tokenization, embeddings, and multi-head attention, hand-rolled from first principles.

**LLM**: Full GPT-style transformer blocks: real self-attention, real generation, not a wrapper.

**Inference & Optimization**: Profiling, quantization, KV-cache, and the optimizers (SGD, Adam, AdamW, Lion, Muon) that make it all run at production speed.

Zero PyTorch. Zero TensorFlow. Every line is yours.

---

## Current Status

| Ready | In Progress | Coming Soon |
|---|---|---|
| All 20 modules implemented | Documentation polish | Community leaderboard |
| Module, CLI, integration, and milestone tests | Edge-case hardening | More milestone exercises |
| `tren` CLI for the full workflow | Performance tuning | Milestones beyond MLPerf |
| Historical milestone scripts | | |

Want to explore the code first? See [Repository Structure](#repository-structure), or the [wiki's Getting Started page](https://github.com/TrenTorch/TrenTorch/wiki/Getting-Started).

---

## 20 Progressive Modules

| Part | Modules | What You Build |
|---|---|---|
| I. Foundations | 01–08 | Tensors, activations, layers, losses, dataloader, autograd, optimizers, training |
| II. Vision | 09 | Conv2d, CNNs for image classification |
| III. Language | 10–13 | Tokenization, embeddings, attention, transformers |
| IV. Optimization | 14–20 | Profiling, quantization, compression, acceleration, memoization, benchmarking, capstone |

Every module asks one question: can you build this from scratch, and build it well?

---

## Historical Milestones

As you progress, you unlock recreations of landmark ML results, run on your own framework:

| Year | Milestone | What You Reproduce |
|---|---|---|
| 1958 | Perceptron | Binary classification with gradient descent |
| 1969 | XOR Crisis | Multi-layer networks solving non-linear problems |
| 1986 | Backpropagation | Multi-layer network training |
| 1998 | CNN Revolution | Image classification with convolutions |
| 2017 | Transformer Era | Language generation with self-attention |
| 2018+ | MLPerf | Production-grade optimization |

Not toy demos: real, historically significant results, on a framework you wrote yourself.

---

## Learning Philosophy

```python
# Most courses:
import torch
model.fit(X, y)  # everything happens somewhere else

# TrenTorch:
# You implement every component
# You measure memory usage
# You optimize performance
# You own every layer of the stack
```

**Why build your own framework?**
- **Deep understanding**: you know exactly what `loss.backward()` does, because you wrote it
- **Systems thinking**: memory, compute, and scaling stop being abstractions
- **Debugging at any depth**: fix problems at the model level or the tensor level
- **Production instincts**: the same patterns real ML systems run on

---

## Repository Structure

```text
TrenTorch/
├── TrenTorch_CLI/                # The `tren` CLI and framework curriculum
│   ├── data/
│   │   ├── src/                      # Curriculum source (edit here)
│   │   │   ├── 01_tensor/
│   │   │   ├── 02_activations/
│   │   │   ├── ...                       # 03-20: layers through capstone
│   │   │   └── 20_capstone/
│   │   ├── modules/                  # Generated notebooks (student-facing, stub-only)
│   │   ├── solutions/                # Reference implementations (maintainer/CI-only)
│   │   ├── datasets/                 # Curated training data (tinydigits, tinytalks)
│   │   ├── milestones/               # Historical ML recreations
│   │   └── trentorch/                # Generated package (import from here)
│   ├── platforms/
│   │   ├── cli/                      # The `tren` CLI itself
│   │   │   ├── main.py
│   │   │   ├── core/                     # Shared plumbing: config, console, theme, runtime
│   │   │   ├── commands/                 # base.py, export_utils.py, jupyter.py
│   │   │   ├── cli_platform/             # Setup, system, package, dev tooling
│   │   │   ├── processes/                # module_workflow, milestone, benchmark, olympics, convert
│   │   │   └── tests/
│   │   └── dev_tools/                # Maintainer scripts
│   ├── user_data/                    # Your own progress and benchmarks (not committed)
│   └── tests/                        # Integration, e2e, and environment tests
│
├── TrenTorch_Web/                 # The browser version (SvelteKit, trentorch.com)
│   ├── platform/                      # Routes, components, assets
│   ├── processes/                     # IDE content, POTD, auth, progress tracking
│   ├── data/app_data/                 # Curriculum content compiled for the browser
│   └── supabase/migrations/           # Auth + user-data schema and RLS policies
│
└── .github/                       # CI/CD shared across both
```

CLI workflow: `TrenTorch_CLI/data/src/*.py` → `TrenTorch_CLI/data/modules/*.ipynb` (you solve it) → `TrenTorch_CLI/data/trentorch/*.py`

---

## Credit

TrenTorch is our implementation, built on the curriculum and foundation of [TinyTorch](https://mlsysbook.ai/tinytorch), created by [Prof. Vijay Janapa Reddi](https://vijay.seas.harvard.edu) and the [ML Systems Book](https://mlsysbook.ai) community at Harvard University.

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
        <sub>Issues: 11 &middot; PRs: 13</sub>
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
        <sub>Issues: 12 &middot; PRs: 145</sub>
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

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Participation in issues, pull requests, and discussions is expected to stay within it.

---

<div align="center">

<b>Build it yourself. Understand it fully.</b>

</div>
