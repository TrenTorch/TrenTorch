# Restructuring Methodology

How the curriculum tracks were merged, renamed and expanded, written down so the same pass can be repeated on any other track. It complements [README.md](README.md), which describes the file formats. This file describes the **decisions** and the **checks**.

## 1. The shape we are aiming for

The hierarchy is fixed at four levels and every level is a folder:

```
<NN>-<track>/                      e.g. 03-data-science
  <NN>-<section>/                  e.g. 01-data-preparation
    <NN>-<sub-section>/            e.g. 02-feature-processing
      <NN>-<question>/             e.g. 04-skew-transforms
```

- A **track** is a root such as Python or Mathematics. A **section** is a broad area. A **sub-section** is one coherent topic. A **question** is one concept with code, tests and theory.
- Every track, section and sub-section folder has a `meta.json` (`title`, and optionally `topics` and `companies`, inherited by everything below). A question folder has **no** `meta.json`: its `README.md` frontmatter already holds its metadata.
- Numeric prefixes only set order. They are stripped by the build, so renumbering never changes an identity.
- A folder with only a `meta.json` and no questions is a placeholder and is skipped by the build.

## 2. Sizing rules

| Rule                                              | Value                                                                                                                                                                |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Questions per sub-section                         | 4 to 6 is comfortable, up to 8 when the topic is broad                                                                                                               |
| "Assemble" capstones per sub-section              | At most 2, and only when they test different capabilities (two pipelines that exercise different skills may both stay)                                               |
| A sub-section already inside the range            | Leave its structure alone. Only rename titles and folders                                                                                                            |
| A sub-section below the range                     | Acceptable when concepts are still missing. Do not merge just to hit a number                                                                                        |
| A section whose name repeats its only sub-section | Avoid it. Split the section into real sub-sections (Preprocessing > Data Preprocessing became Data Preparation > Cleaning, Feature Processing, Sampling & Splitting) |

## 3. Naming and writing rules

These apply to every title, folder name, heading and sentence you write.

1. **Titles name the concept or purpose, never a function or method.** "Conditional Selection", not "np.where". "Reordering Axes", not "transpose / .T".
2. **Prefer `&` over "and" in titles and headings.** Not everywhere in prose.
3. **No comma before "and" in a list.** "A, B and C". Keep a comma only where it separates two full clauses.
4. **No em dashes anywhere.** Use a comma, a colon or a new sentence. In titles prefer a colon.
5. **Folder names never contain "and" or "vs".** `iterables-iterators`, not `iterables-vs-iterators`. Keep them short (`04-silent-copies`, not `04-silent-copies-from-non-contiguous-layouts`).
6. **Titles are short.** Drop descriptive tails ("Gaussian Distribution", not "Gaussian Distribution: the bell curve behind noise, errors, and the CLT").
7. **Never delete `.DS_Store` files** and never commit them. If a folder must be removed and it holds one, move the file aside rather than deleting it.

## 4. Deciding what to merge

Work one sub-section at a time.

1. **Read every question's title and Statement** and write down the idea it teaches in one phrase.
2. **Group questions that teach one idea.** Typical merges: a concept and its sibling operation (adding & removing elements), a concept and its numeric twin (a population version and a sample version), a definition and its immediate application, a theory question and its "contrast note".
3. **Keep apart** questions that need different mental models, even if they share a topic word.
4. **Keep one capstone per distinct capability.** Fold two capstones into one only when they exercise the same skills.
5. **Respect the core-then-library split.** Core mechanics are taught per topic first (lists, comprehensions, views vs copies). How libraries implement the same idea (NumPy, later PyTorch) lives in the Data Libraries sections. Do not delete one because the other exists.
6. **Name the merged question after the idea, and pick its `name`.** If an external reference only needs the first part, reuse that part's old `name` to keep the ripple small. Otherwise choose a new unique `name` and remap every reference (section 7).

### Mechanics of a merge

A merged question is one folder with one `README.md`, `starter.py`, `solution.py` and `tests.py`.

- **README, Python style:** one Statement sentence you write that lists what the parts do, then `###` sub-headings in Theory (one per original topic), then the original Explanation paragraphs joined.
- **README, math and data-science style:** the Statement keeps its four sections (`The problem, from first principles`, `From theory to code`, `Constraints`, `Hints`). Under each, every part appears with a bold label (`**Part name**`). Theory is merged by heading name (`The simple version`, `The formula`, part-specific headings kept as they are, `How NumPy/PyTorch actually implements this` last). Explanation paragraphs are labelled per part. Frontmatter tags are the union and difficulty is the highest.
- **Code files:** concatenate in order, hoist and de-duplicate `import` lines.
- **Tests:** one header (docstring, imports, `_module = load_solution(__file__)`, then every `name = _module.name` alias), then the test bodies in order.

After merging, always check these four things, because each caused a real failure:

1. **Duplicate test names.** Two functions with the same name silently shadow each other and drop a test. Rename one.
2. **Duplicate function names with different meanings** (two `covariance` functions, one for a joint table and one for samples). Rename one (`pmf_covariance`) and update its tests, README text and Explanation.
3. **A solution or starter that loaded a sibling by name** (`load_solution("old-sibling")`). The sibling now lives in the same file, so delete those lines, otherwise the module loads itself and recurses.
4. **An alias written as `x = load_solution(__file__).x`** in the middle of a test file. The in-browser runner only handles aliases in the header. Convert it to `x = _module.x` and move it to the header.

## 5. Adding missing concepts

Add questions only for concepts a learner of that sub-section would expect and cannot find. Decide the list with the maintainer first. Each new question follows the same format as its neighbours.

**README sections**

- `## Statement`: the contract only, never the formula or the one-line answer.
  - `### The problem, from first principles`: a concrete motivation, linked back to the neighbouring question.
  - `### From theory to code`: names the functions to implement and says the signatures are in the editor.
  - `### Constraints`: every rule a hidden test relies on (shapes, tie rules, error cases, draw order for random numbers).
  - `### Hints`: two to four `<details>` blocks, each giving away a little more.
- `## Theory`: `The simple version` (an analogy), `The formula` (LaTeX), one or two topic sections, `How NumPy/PyTorch actually implements this`.
- `## Explanation`: why the oracle solution is written the way it is.

**Tests**

- At least a dozen. Cover correctness on a hand-computed case, shapes, edge cases, and a "mutation-catching" case that fails if a natural mistake is made (summing instead of averaging, forgetting to shuffle).
- Include an **independent oracle**: a second, plainly written implementation inside the test, or a comparison with NumPy.
- For anything random, **pin the order of random draws in the Constraints** (`step = rng.normal()` then `u = rng.random()`) so a seeded test can replay them. Pass the generator in, never use global state.
- Assert that inputs are **not modified**.
- Use plain `assert`, `np.isclose`, `np.testing.assert_allclose` and `pytest.raises`. **Never use `pytest.mark`, fixtures or `pytest.approx`**: the in-browser runner (Pyodide) lacks them.
- Use only NumPy and the standard library in solutions. Pyodide does not ship everything CPython does.
- Do not assert wall-clock speed with tight margins. CI runners are noisy.
- Visualization questions cannot assert on a drawn chart. Test the numbers behind it (bin edges, quartiles, density values, quantiles).

**Naming**

- `name:` in the frontmatter is global and unique. Use a stable prefix for the track (`math-`, `data-science-`, `numpy-`).
- The folder slug is for humans and order only. Nothing may depend on it.

## 6. Moving content between tracks

- Moving a folder never changes its `name`, so tests that load by name keep working.
- Update `meta.json` `topics` so the topic filter still matches.
- Renumber siblings so numbering has no gaps.
- If a sub-section holds content from another discipline (NumPy memory inside resource management), propose the move to the maintainer before making it.

## 7. Keeping references valid

Renaming or merging is only safe once every reference is updated. Search the whole repository for each retired `name` and each retired folder slug.

| Where references live                                                                            | What to do                                                                                        |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| `load_solution("old-name")` in other questions' `solution.py`, `starter.py`, `tests.py`          | Replace with the new name (use a lookahead so `math-x` does not match `math-x-covariance`)        |
| Backticked folder slugs in README text (`` `04-joint-and-marginal-probability` ``)               | Map old slug to new slug inside the affected track. Stale numbering already exists, so map it too |
| Interactive widgets keyed by question name (`platform/widgets/*-visualizer-ids.js`)              | Do **not** rename the widget ids. Embed a placeholder instead (below)                             |
| Specs that use a real question as a fixture (`processes/ide-content/build-test-harness.spec.ts`) | Point them at the new name                                                                        |

**Widgets in merged questions.** A visualizer is mounted from its id. When topics merge, put one placeholder per topic at the end of that topic's Theory:

```html
<div class="tt-widget" data-widget="math-bayes-theorem"></div>
```

`GuidePane.svelte` mounts every registered `data-widget` it finds (`embeddedWidgetIds` in `platform/widgets/registry.js`). A merged question must **not** declare a `widget:` in its frontmatter, because a single declared widget takes precedence and hides the others. The visualizer specs accept an id that is either a question id or embedded in a question's Theory.

## 8. Build, regenerate, verify

Run from `TrenTorch_Web/`. These mirror CI (`.github/workflows/ci.yml`), so run all of them before pushing.

```bash
npm run curriculum:build                                       # validate every root, section, track and question
npm run lint                                                   # prettier --check on every file, then eslint
npx dotenvx run -f .env.test -- npm run check                  # svelte-check
npx dotenvx run -f .env.test -- npm run test                   # vitest
npx dotenvx run -f .env.test -- npm run build && npm run test:smoke
npm run test:pyodide                                           # every question run in the browser runtime
python -m pytest data/app_data -q -n 2                         # every question's own tests against its solution
```

Practical notes:

- Prettier checks **every** data file, including each `meta.json` and every README. Run `npx prettier --write` on the files you touch, or the Lint step fails first and hides every later step.
- The curriculum is not committed as generated JSON. The app compiles `data/app_data` in memory (`processes/curriculum-build/vite-plugin-curriculum.mjs`), so there is no step to run after an edit: the dev server reloads on save, and a build compiles the current sources.
- The CI test dependencies are hash-pinned for Linux. On macOS install the same versions without hashes (`pip install numpy==... pytest==...`).
- Cache folders (`__pycache__`, `.pytest_cache`) may be removed. `.DS_Store` files may not.
- Commit messages and PR descriptions must **not** contain `Co-Authored-By:` AI trailers or "Generated with" footers. CI rejects them and a fix needs a force-push.
- Some timing-based tests in unrelated tracks are flaky on shared runners. Re-run the failed job before investigating.

## 9. A repeatable procedure for one track

1. List the track's sections, sub-sections and questions with titles, names and difficulty. Note which have widgets and which are referenced from elsewhere.
2. Decide the target structure (sections 1 and 2). If the track has content that belongs elsewhere, or if structure choices are not obvious, ask the maintainer before moving anything.
3. Move folders into the new layout and write the `meta.json` files (tab indentation, `title`, inherited `topics` and `companies`).
4. Merge questions (section 4), then rename titles and folders (section 3).
5. Remap references (section 7), regenerate, and run the unit tests of every touched question.
6. Add the agreed new questions (section 5), each tested against its own oracle.
7. Strip em dashes and Oxford commas, change "and" to `&` in titles and headings, and run prettier.
8. Run the full verification list (section 8).
9. Commit in two or three commits separated by purpose: content restructure, platform change (if any), and the regenerated bundle.

## 10. What was applied, track by track

**Python.** Semantics 62 questions to 38, with Basics, Strings, Lists, Tuples, Dictionaries, Sets, Functions and Errors & Exceptions as sub-sections. Object mechanics, resource management and packaging were tidied. NumPy memory moved into Data Libraries as Performance & Memory, and the Data Libraries sub-sections were renumbered 01 to 08 and renamed after concepts.

**Mathematics.** Probability 16 questions to 8, with merged questions keeping one visualizer per part (section 7). Batch, mini-batch and stochastic gradient descent became three questions on one linear-regression setup. Geometric, telescoping, Fourier and generating-function questions were added after Taylor. Linear algebra gained Householder reflections, Householder QR and the full set of definiteness questions.

**Data Science.** Reorganised into Exploratory Data Analysis (EDA), Visualization, Data Preparation and Data Storage & Retrieval, in that order. The four Tabular Foundation Models questions are model architectures, so they moved to Deep Learning (a new Architectures section) with their names unchanged. Existing questions: 15 became 13 (missing-value detection and imputation merged, tabular in-context prediction and its contrast note merged). Questions added: Missingness Patterns, Ordinal & Target Encoding, Skew Transforms, Feature Selection, Train, Validation & Test Splits, Class Imbalance, Categorical Association, Monte Carlo Estimation, Importance Sampling, Markov Chain Monte Carlo, Histogram Bins, Box Plot Statistics, Empirical CDF, Kernel Density Estimation and Quantile-Quantile Plots. Data Storage & Retrieval is an umbrella section with two sub-sections, both implemented from scratch: Data Structures (Hash Tables, Binary Search & Sorted Indexes, Heaps & Top-K, LRU Cache, Bloom Filters) and Databases (Joins, Group-By & Aggregation, Window Functions, B-Tree Indexes, Row & Columnar Storage, Transactions, Query Execution Pipeline).

## 11. Pitfalls that actually happened

- A merged test file lost a test because two functions shared a name.
- A merged solution recursed forever because it still loaded its former sibling by name.
- Prettier rewrote 127 data files at the start of a PR, which turned the first CI step red.
- `pytest.mark.parametrize` passed locally and failed in the browser runner.
- A generated bundle committed from a tree with a stray local edit failed `curriculum:check`.
- AI co-author trailers made a CI check fail until the commit messages were rewritten.
- A shell `rm -r` on a folder holding a `.DS_Store` file prompted and hung. Move the file aside instead of removing it.
