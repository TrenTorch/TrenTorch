# Contributing to TrenTorch

Thanks for your interest in contributing. By participating, you agree to uphold the [Code of Conduct](../../CODE_OF_CONDUCT.md).

TrenTorch is an educational ML project, so every contribution should make things clearer for someone learning, not just more correct in the abstract:

- **Enhance learning**: make concepts clearer for students
- **Preserve the learning progression**: don't skip ahead of what a module has taught by that point
- **Keep it simple**: educational clarity over production complexity

## How to contribute

Every change starts with an issue and ends with a merged PR. The order matters, because it keeps two people from fixing the same bug and lets a maintainer catch a wrong approach before you have spent time on it.

1. **Raise an issue.** Check the open issues first so you don't duplicate one. Then use the bug report form and cover three things:
   - **What is wrong.** What happened, and what you expected instead.
   - **Everything needed to recreate it.** The exact `tren` commands, notebook cells, or steps on the site (with the question URL), the full error output, your OS, and your `tren --version` and `python --version` (or your browser, for the web app).
   - **How big it is.** Pick a severity from the table below.

   Make the last line of the issue a clear choice: **"I want to work on this"** or **"I want someone else to solve this"**.

2. **If you want to solve it, describe your approach.** Write how you plan to fix it in the issue, and ask the maintainers whether that approach is correct. Do not start the PR yet.

3. **Wait for approval and assignment.** A maintainer replies to say the approach is right (or suggests a different one) and assigns the issue to you. Only the assigned person works on an issue.

4. **Open the PR.** Once you are assigned, branch off `TrenTorch-Dev`, make the change, and open a PR that references the issue (for example `Fixes #123`). The maintainers review it. They will either request changes, or make the changes themselves, and then merge it.

5. **Keep it moving.** If you are assigned an issue and there is no PR for it within **3 days**, the issue is stale and it goes to someone else. A draft PR counts as work in progress. If you can no longer work on it, say so in the issue and someone else will take it. There is no penalty for handing an issue back.

6. **Do not take an issue that is assigned to someone else.** If an issue is assigned, it is taken. Opening a PR for another person's assigned issue is not allowed, and the maintainers may block you from the TrenTorch organization for it. If an issue looks abandoned, comment on it and ask. After 3 days without a PR, it is unassigned automatically.

Security problems do **not** go through a public issue. Follow [`SECURITY.md`](../../SECURITY.md).

### Severity

| Severity | What it means |
|---|---|
| Critical | The CLI or site is unusable, data is lost or wrong, or a question's tests are wrong for every student |
| Major | A core feature or a whole module or question fails, and there is no reasonable workaround |
| Minor | Something is wrong or confusing, but there is a workaround |
| Cosmetic | Typos, wording, layout, or docs that don't change behavior |

## Getting started

```bash
git clone https://github.com/TrenTorch/TrenTorch.git
cd TrenTorch/TrenTorch_CLI
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e ./
```

Then verify it works:

```bash
tren --version
tren system health
tren module status
```

For the web app:

```bash
cd TrenTorch_Web
npm install
npm run dev
```

Sign-in uses Supabase. Copy `.env.example` to `.env` and add your own project keys to use it locally.

Also worth a look: [`design.md`](design.md) (educational context and teaching approach), the [README](../../README.md) (repository structure), and the [wiki](https://github.com/TrenTorch/TrenTorch/wiki) (curriculum overview, CLI reference, architecture).

## Workflow

```bash
git checkout TrenTorch-Dev
git pull origin TrenTorch-Dev
git checkout -b your-github-username/your-improvement

# make your changes, then test them
pytest tests/
tren module test 01

git add <specific-files>    # not `git add .`, stage files explicitly
git commit -m "fix: correct tensor broadcasting in module 02"
git push origin your-github-username/your-improvement
# then open a PR on GitHub targeting TrenTorch-Dev
```

- **Target branch**: `TrenTorch-Dev` is the default branch and where PRs go, unless the issue says otherwise. `TrenTorch-Main` is only updated by maintainers once things are stable.
- **Branch names**: `<github-username>/<feature-name>`, lowercase, hyphens (for example `shivtej/fix-attention-mask`). Your username first, always.
- **PR titles** follow [Conventional Commits](https://www.conventionalcommits.org/) (`fix:`, `feat:`, `docs:`, `ci:`, and so on). A check enforces it.
- **No AI co-author trailers.** A check rejects commits that credit an AI tool as a co-author or carry a "Generated with" footer.
- **Never work directly on `TrenTorch-Dev` or `TrenTorch-Main`.**
- **Always use the virtual environment.**

## Testing

CLI:

```bash
tren module test NN          # for example: tren module test 01, one module's own tests
pytest tests/integration/    # cross-module integration tests
pytest tests/                # everything: integration, regression, e2e
pytest platforms/cli/tests/  # the tren CLI's own test suite
```

Web (run from `TrenTorch_Web/`):

```bash
npm run check          # types
npm run lint           # prettier and eslint
npm run test           # unit tests
npm run test:pyodide   # runs every question's solution and tests in a real Pyodide
```

CI has to be green before a PR merges. See it run on your own PR rather than only trusting local results.

## Code standards

**Students** (using the framework): work in `data/modules/NN_name/name.ipynb` in Jupyter, and export with `tren module complete N`.

**Contributors** (improving the framework itself): edit `data/src/NN_name/NN_name.py` (the source of truth). Notebooks are generated from it with `tren dev export`. Include:

- immediate tests after each implementation
- memory and performance analysis where it fits the module's own systems focus
- clear explanations, because clarity is the point of this codebase

Web question content lives under `TrenTorch_Web/data/app_data/`. The [authoring guide](../../TrenTorch_Web/data/app_data/README.md) explains the layout.

## Opening a pull request

Describe what changed and why, and how you tested it. Confirm `ruff check` and `ruff format --check` pass locally (a bot also runs them and pushes straightforward fixes onto your branch). Keep the PR to one thing: a bug fix and an unrelated refactor in the same PR is harder to review and harder to revert.

Reference the issue you were assigned (`Fixes #123`). A bot checks this for external contributors and comments on the PR if the issue is missing, or if it is assigned to someone else. Every PR needs at least one approving review from someone other than its author before it can merge.

## Releases (maintainers)

[Semantic versioning](https://semver.org/): patch for fixes, minor for new features or modules, major for breaking changes. There is no automated release pipeline yet: `pyproject.toml`'s version is bumped by hand, and changes land by merging to `TrenTorch-Main` once CI is green. Contributors don't need to think about version bumps.

---

**Questions?** Open a [GitHub Discussion](https://github.com/TrenTorch/TrenTorch/discussions), or check the wiki.
