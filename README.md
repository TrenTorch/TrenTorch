<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/hero-dark.svg" />
  <img src=".github/assets/hero-light.svg" width="100%" alt="TrenTorch: learn ML by building it" />
</picture>

**Learn ML by building it: a from-scratch machine learning framework in NumPy, and hundreds of coding questions that run in your browser.**

[![CI](https://github.com/TrenTorch/TrenTorch/actions/workflows/validate.yml/badge.svg?branch=TrenTorch-Dev)](https://github.com/TrenTorch/TrenTorch/actions/workflows/validate.yml)
[![Problems](https://img.shields.io/endpoint?url=https%3A%2F%2Ftrentorch-status.shashanktripathi07.workers.dev%2Fapi%2Fbadge%2Fproblems)](https://trentorch.com)
[![Contributors](https://img.shields.io/badge/contributors-22-orange.svg)](#team-engineers)
[![CodeFactor A+](https://img.shields.io/badge/CodeFactor-A%2B-2ecc71?logo=codefactor&logoColor=white)](https://www.codefactor.io/repository/github/trentorch/trentorch)
[![Python](https://img.shields.io/badge/python-3.10+-3776ab?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/license-PolyForm--Noncommercial--1.0.0-blue.svg)](LICENSE)

<a href="https://vercel.com/oss"><img src="https://vercel.com/oss/program-badge-2026.svg" height="24" alt="Vercel OSS Program" /></a>

[Try it in the browser](https://trentorch.com) · [Quickstart](#quickstart) · [Curriculum](#curriculum) · [Contributing](#contributing) · [FAQ](#faq)

<table>
  <tr>
    <td align="center" width="170"><b><!-- question-count -->1647<!-- /question-count --></b><br /><sub>coding problems</sub></td>
    <td align="center" width="170"><b>12</b><br /><sub>topic areas</sub></td>
    <td align="center" width="170"><b>20</b><br /><sub>framework modules</sub></td>
    <td align="center" width="170"><b>0</b><br /><sub><code>import torch</code> needed</sub></td>
  </tr>
</table>

<p>
  <img src=".github/assets/screenshot-questions.png" width="49%" alt="The TrenTorch questions page: a list of tracks with question counts and a progress bar" />
  <img src=".github/assets/screenshot-ide.png" width="49%" alt="The TrenTorch in-browser editor: problem statement on the left, Python editor and test results on the right" />
</p>

</div>

---

> [!NOTE]
> The CLI curriculum is our implementation of [TinyTorch](https://mlsysbook.ai/tinytorch) (Harvard CS249r), rebuilt and extended in our own style. The browser version is our own, built independently.

## Quickstart

**In the browser:** open [trentorch.com](https://trentorch.com), sign in with GitHub, Google, or email, and start a question. Nothing to install. Python runs in your browser (Pyodide) and your code is graded instantly.

**In your terminal:**

```bash
git clone https://github.com/TrenTorch/TrenTorch.git
cd TrenTorch/TrenTorch_CLI
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install -e .
tren setup
tren module start 01
```

<details>
<summary>Windows (PowerShell)</summary>

```powershell
git clone https://github.com/TrenTorch/TrenTorch.git
cd TrenTorch\TrenTorch_CLI
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
tren setup
tren module start 01
```

</details>

`tren setup` adds `tren` to your PATH, so later terminals just need `tren`, no activating first. The [command reference](TrenTorch_CLI/docs/command-reference.md) covers the rest (`tren tui`, `tren serve`, `tren milestone`, `tren benchmark`).

<details>
<summary>Run the web app locally</summary>

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

</details>

## Why build it yourself

Most people learn ML frameworks by importing them. We wanted to know how they work, so we built one. Every operation traces back to raw NumPy, the architecture matches what production frameworks use, and there is no `import torch` anywhere in the curriculum. You know what `loss.backward()` does because you wrote it.

<table>
  <tr>
    <td valign="top" width="33%"><b>1. Pick a problem</b><br /><sub>Each one comes with a problem statement, a theory section and a starter file.</sub></td>
    <td valign="top" width="33%"><b>2. Write the code</b><br /><sub>Python runs in your browser (Pyodide), or in your terminal with the CLI. Nothing to set up for the web version.</sub></td>
    <td valign="top" width="33%"><b>3. Get graded</b><br /><sub>Tests run instantly, and a reference solution is there once you want to compare.</sub></td>
  </tr>
</table>

## Curriculum

The same ground, two ways:

| | [TrenTorch Web](https://trentorch.com) | TrenTorch CLI |
|---|---|---|
| **Where** | Your browser | Your terminal and Jupyter |
| **What** | <!-- question-count -->1647<!-- /question-count --> coding problems in 12 topic areas | 20 modules that build a framework, from tensors to a capstone |
| **Progress** | Saved to your account | Saved locally under `user_data/` |
| **Code** | [`TrenTorch_Web/`](TrenTorch_Web) (SvelteKit) | [`TrenTorch_CLI/`](TrenTorch_CLI) (Python) |

A **Problem of the Day** features one new web question every day.

<details>
<summary>Web: 12 topic areas and their tracks</summary>

Every question has a problem statement, a theory section, a starter file, tests, and a reference solution.

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

</details>

<details>
<summary>CLI: 20 modules</summary>

| Part | Modules | What you build |
|---|---|---|
| I. Foundations | 01-08 | Tensors, activations, layers, losses, dataloader, autograd, optimizers, training |
| II. Vision | 09 | Conv2d, CNNs for image classification |
| III. Language | 10-13 | Tokenization, embeddings, attention, transformers |
| IV. Optimization | 14-20 | Profiling, quantization, compression, acceleration, memoization, benchmarking, capstone |

</details>

<details>
<summary>CLI: historical milestones</summary>

As you progress, you unlock recreations of landmark ML results, run on your own framework:

| Year | Milestone | What you reproduce |
|---|---|---|
| 1958 | Perceptron | Binary classification with gradient descent |
| 1969 | XOR Crisis | Multi-layer networks solving non-linear problems |
| 1986 | Backpropagation | Multi-layer network training |
| 1998 | CNN Revolution | Image classification with convolutions |
| 2017 | Transformer Era | Language generation with self-attention |
| 2018+ | MLPerf | Production-grade optimization |

</details>

<details>
<summary>Repository structure</summary>

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

</details>

<details>
<summary>CLI: how a module flows</summary>

```mermaid
flowchart TD
    src["data/src/NN_name.py<br/>curriculum source"] -->|"built into"| nb["data/modules/*.ipynb<br/>stubs for you to fill in"]
    nb -->|"tren module start NN"| you(["You implement it"])
    you -->|"tren module complete NN<br/>(tests, then export)"| pkg["data/trentorch/*.py<br/>your own framework"]
    pkg -->|"unlocks"| ms["tren milestone run<br/>landmark ML results"]
```

</details>

## Contributing

Issues and pull requests are welcome. Start with the [contributing guide](TrenTorch_CLI/docs/CONTRIBUTING.md): open an issue first, and ask to be assigned before you start on it. CI has to be green and one review from someone other than the author is required to merge. The first-contribution bot greets you on your first PR. Code quality is tracked on [CodeFactor](https://www.codefactor.io/repository/github/trentorch/trentorch), where the repository is graded A+.

Found a security problem? Do not open a public issue. Read [SECURITY.md](SECURITY.md).

---

## Team Engineers

The maintainers, code owners first and then most active first (PRs plus issues). Counts are recomputed whenever a PR merges, from real issue/PR activity via [`.github/workflows/update-contributors.yml`](.github/workflows/update-contributors.yml).

<div align="center">

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="50.0%">
        <a href="https://github.com/Shashank-Tripathi-07"><img src=".github/assets/avatars/Shashank-Tripathi-07-card.svg" width="209" height="197" alt="Rocky"/></a>
        <br />
        <sub><strong>Principal Maintainer &amp; Infrastructure Architect</strong></sub>
        <br />
        <sub>IIT Guwahati<br />Debugs autograd for fun, ships before sunrise</sub>
        <br />
        <sub>Issues: 18 &middot; PRs: 203</sub>
        <br />
        &nbsp;
      </td>
      <td align="center" valign="top" width="50.0%">
        <a href="https://github.com/ShivtejG236"><img src=".github/assets/avatars/ShivtejG236-card.svg" width="209" height="197" alt="Shivtej Gaikwad"/></a>
        <br />
        <sub><strong>Maintainer &amp; Head of EngOps</strong></sub>
        <br />
        <sub>IIT Guwahati<br />Shows up, builds systems, moves on to the next thing</sub>
        <br />
        <sub>Issues: 6 &middot; PRs: 99</sub>
        <br />
        &nbsp;
      </td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td align="center" valign="top" width="50.0%">
        <a href="https://github.com/maanas1234"><img src=".github/assets/avatars/maanas1234-card.svg" width="209" height="197" alt="Maanas Tyagi"/></a>
        <br />
        <sub><strong>Maintainer &amp; Core Engineer</strong></sub>
        <br />
        <sub>Catches bugs, builds solutions &amp; ships fast</sub>
        <br />
        <sub>Issues: 14 &middot; PRs: 69</sub>
        <br />
        &nbsp;
      </td>
      <td align="center" valign="top" width="50.0%">
        <a href="https://github.com/aadityansha06"><img src=".github/assets/avatars/aadityansha06-card.svg" width="209" height="197" alt="Aadityansha"/></a>
        <br />
        <sub><strong>Maintainer &amp; Growth Lead</strong></sub>
        <br />
        <sub>Processor engineer, breathes Assembly &amp; CUDA</sub>
        <br />
        <sub>Issues: 1 &middot; PRs: 16</sub>
        <br />
        &nbsp;
      </td>
    </tr>
  </tbody>
</table>

</div>

---

## Open-Source Contributors

Everyone else who has had a PR merged, most active first (PRs plus issues), or is credited as a `Co-authored-by:` on one. Want to show up here? Get a PR merged, or get credited as a co-author on someone else's: the first-contribution bot will say hello on your first PR, and this grid updates automatically after it merges. A closed-without-merging PR doesn't count, and neither does an issue on its own.

<details>
<summary>Show all 18 contributors</summary>

<div align="center">

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/JashT14"><img src=".github/assets/avatars/JashT14.svg" width="96" height="96" alt="JashT14"/></a>
        <br />
        <b>JashT14</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 10 &middot; PRs: 3</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/AllenGeorge08"><img src=".github/assets/avatars/AllenGeorge08.svg" width="96" height="96" alt="AllenGeorge08"/></a>
        <br />
        <b>AllenGeorge08</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 2 &middot; PRs: 4</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/VrajVed"><img src=".github/assets/avatars/VrajVed.svg" width="96" height="96" alt="VrajVed"/></a>
        <br />
        <b>VrajVed</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 1 &middot; PRs: 2</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/KeuqS"><img src=".github/assets/avatars/KeuqS.svg" width="96" height="96" alt="KeuqS"/></a>
        <br />
        <b>KeuqS</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 2</sub>
      </td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/lux-liang"><img src=".github/assets/avatars/lux-liang.svg" width="96" height="96" alt="lux-liang"/></a>
        <br />
        <b>lux-liang</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 2</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/shivamraut747-ux"><img src=".github/assets/avatars/shivamraut747-ux.svg" width="96" height="96" alt="shivamraut747-ux"/></a>
        <br />
        <b>shivamraut747-ux</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 2</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/NaveenChandraAdhikari"><img src=".github/assets/avatars/NaveenChandraAdhikari.svg" width="96" height="96" alt="NaveenChandraAdhikari"/></a>
        <br />
        <b>NaveenChandraAdhikari</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 1 &middot; PRs: 1</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/pendi1901"><img src=".github/assets/avatars/pendi1901.svg" width="96" height="96" alt="pendi1901"/></a>
        <br />
        <b>pendi1901</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 1 &middot; PRs: 1</sub>
      </td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/ReetikaMishra23"><img src=".github/assets/avatars/ReetikaMishra23.svg" width="96" height="96" alt="ReetikaMishra23"/></a>
        <br />
        <b>ReetikaMishra23</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 1 &middot; PRs: 1</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/Shreyacodess20"><img src=".github/assets/avatars/Shreyacodess20.svg" width="96" height="96" alt="Shreyacodess20"/></a>
        <br />
        <b>Shreyacodess20</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 1 &middot; PRs: 1</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/abhay2geek"><img src=".github/assets/avatars/abhay2geek.svg" width="96" height="96" alt="abhay2geek"/></a>
        <br />
        <b>abhay2geek</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 1</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/bernalalexis-try"><img src=".github/assets/avatars/bernalalexis-try.svg" width="96" height="96" alt="bernalalexis-try"/></a>
        <br />
        <b>bernalalexis-try</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 1</sub>
      </td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/devsterxyz"><img src=".github/assets/avatars/devsterxyz.svg" width="96" height="96" alt="devsterxyz"/></a>
        <br />
        <b>devsterxyz</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 1</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/MahekPatel-2403"><img src=".github/assets/avatars/MahekPatel-2403.svg" width="96" height="96" alt="MahekPatel-2403"/></a>
        <br />
        <b>MahekPatel-2403</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 1</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/mayuriphad"><img src=".github/assets/avatars/mayuriphad.svg" width="96" height="96" alt="mayuriphad"/></a>
        <br />
        <b>mayuriphad</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 1</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/MayurK-cmd"><img src=".github/assets/avatars/MayurK-cmd.svg" width="96" height="96" alt="MayurK-cmd"/></a>
        <br />
        <b>MayurK-cmd</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 1</sub>
      </td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/pushkarkumarvats"><img src=".github/assets/avatars/pushkarkumarvats.svg" width="96" height="96" alt="pushkarkumarvats"/></a>
        <br />
        <b>pushkarkumarvats</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 1</sub>
      </td>
      <td align="center" valign="top" width="25.0%">
        <a href="https://github.com/Saaarthak0102"><img src=".github/assets/avatars/Saaarthak0102.svg" width="96" height="96" alt="Saaarthak0102"/></a>
        <br />
        <b>Saaarthak0102</b>
        <br />
        <sub>Spots bugs, fixes them &amp; contributes</sub>
        <br />
        <sub>Issues: 0 &middot; PRs: 1</sub>
      </td>
    </tr>
  </tbody>
</table>

</div>

</details>

---

## Credit

TrenTorch's CLI is our implementation, built on the curriculum and foundation of [TinyTorch](https://mlsysbook.ai/tinytorch), created by [Prof. Vijay Janapa Reddi](https://vijay.seas.harvard.edu) and the [ML Systems Book](https://mlsysbook.ai) community at Harvard University.

<details>
<summary>Related educational frameworks</summary>

- [tinygrad](https://github.com/tinygrad/tinygrad): George Hotz's minimalist framework
- [micrograd](https://github.com/karpathy/micrograd): Andrej Karpathy's tiny autograd
- [MiniTorch](https://minitorch.github.io/): Cornell's educational framework

</details>

## License

[PolyForm Noncommercial License 1.0.0](LICENSE): free for personal, educational, and noncommercial use. Not licensed for commercial use.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). It applies in issues, pull requests, discussions, and on [trentorch.com](https://trentorch.com).

## FAQ

<details>
<summary>Is TrenTorch free?</summary>

Yes, for personal, educational, and noncommercial use, under the [PolyForm Noncommercial License 1.0.0](LICENSE). Commercial use is not covered. If you want to use it in a paid course or inside a company, get in touch at [rocky@trentorch.com](mailto:rocky@trentorch.com) or through [trentorch.com/contact](https://trentorch.com/contact).

</details>

<details>
<summary>Web or CLI: which should I start with?</summary>

Start with the web app if you want to try questions right now with nothing to install. Use the CLI if you want to build the framework yourself, module by module, in notebooks on your own machine. They cover the same ground, and progress is not shared between them.

</details>

<details>
<summary>Do I need a GPU, PyTorch, or TensorFlow?</summary>

No. Everything runs on the CPU with NumPy, and the curriculum never imports PyTorch or TensorFlow. The CLI needs Python 3.10 or newer. The web app runs Python 3.12 inside your browser.

</details>

<details>
<summary>Where does my code run on the web app?</summary>

In your browser, using Pyodide (Python compiled to WebAssembly). Running and grading a question does not need a server. Your progress (which questions you have solved) is saved to your account, which you create by signing in with GitHub, Google, or an email link.

</details>

<details>
<summary>How is this different from TinyTorch?</summary>

The CLI curriculum is our own implementation of [TinyTorch](https://mlsysbook.ai/tinytorch) from Harvard's CS249r: same foundation, rebuilt and extended in our style. The web app is a separate, independent project built on its own question bank.

</details>

<details>
<summary>How do I add or fix a question?</summary>

Open an issue first and ask to be assigned, as described in the [contributing guide](TrenTorch_CLI/docs/CONTRIBUTING.md). Web questions are plain files under `TrenTorch_Web/data/app_data/`, and the [authoring guide](TrenTorch_Web/data/app_data/README.md) explains the layout. CLI modules are edited in `TrenTorch_CLI/data/src/`.

</details>

<details>
<summary>How do I get listed under Open-Source Contributors?</summary>

Get a pull request merged. A workflow updates the grid automatically after each merge. A closed-without-merging PR does not count, and neither does an issue on its own.

</details>

<details>
<summary>I found a bug. Where do I report it?</summary>

Open a [GitHub issue](https://github.com/TrenTorch/TrenTorch/issues) with steps to reproduce. For a security problem, do not open a public issue: follow [SECURITY.md](SECURITY.md).

</details>

---

<div align="center">

<b>Build it yourself. Understand it fully.</b>

</div>
