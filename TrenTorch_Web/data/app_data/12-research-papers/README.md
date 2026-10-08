# Research papers: how to add a paper

The `/papers` pages are built from the folders in this directory. To add a paper, or sixty,
add folders and files. No code changes are needed: the index, the paper page and its list of
exercises all appear on the next build.

```
12-research-papers/
  04-some-topic/                      a topic (a card on /papers)
    meta.json                         { "title": "...", "description": "..." }
    03-some-paper/                    a paper (the folder name, minus "03-", is its URL: /papers/some-paper)
      meta.json                       see below
      01-first-exercise/              one coding exercise: README.md, starter.py, solution.py, tests.py
      02-second-exercise/
```

The numeric prefixes only set the order they are shown in.

## Adding a paper

1. Create the folder `<NN>-<paper-slug>` inside the right topic. Use lower-case words joined by `-`.
2. Add `meta.json`. `title` is the short name the curriculum uses; `paper` is what the papers pages show:

```json
{
	"title": "Dropout",
	"topics": [],
	"paper": {
		"title": "Improving neural networks by preventing co-adaptation of feature detectors",
		"authors": "Geoffrey Hinton, Nitish Srivastava, Alex Krizhevsky",
		"year": 2012,
		"kind": "foundational",
		"summary": "One or two sentences on what the paper shows.",
		"arxivId": "1207.0580"
	}
}
```

- `kind` is `foundational` or `breakthrough`.
- `arxivId` has no `arXiv:` prefix and no version (`1207.0580`, not `arXiv:1207.0580v2`).
- Optional `slug` in `paper` sets the URL when it should differ from the folder name.

3. Add one folder per coding exercise (at least one), written like any other question: see
   `data/app_data/README.md`. In each `README.md` the frontmatter needs `name` (a unique id such as
   `research-dropout-forward`), `title` and `difficulty` (`Beginner`, `Intermediate` or `Advanced`).
   A title written as `Paper: Exercise` is shown as just `Exercise` inside that paper's list.

## Adding a topic

Create a folder `<NN>-<topic-slug>` with a `meta.json` holding `title` and `description`, then put papers in it.
A topic with no papers yet is ignored.

## Checking your work

The build validates every file and fails with a message that names the file to fix (missing field,
bad `kind`, duplicate slug, a paper with no exercises, ...). To check without a full build:

```
npx vitest --run processes/papers
```
