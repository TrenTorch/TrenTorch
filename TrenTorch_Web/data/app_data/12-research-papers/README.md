# Adding a research paper

The `/papers` pages are built from the folders in this directory. To add a paper you only add
folders and files. You do not touch any code.

## How it is organised

```
12-research-papers/
  00-neural-network-foundations/        a topic (one card on /papers)
    meta.json                           title + description of the topic
    01-dropout/                         a paper
      meta.json                         the paper's details
      01-dropout-forward/               an exercise (README.md, starter.py, solution.py, tests.py)
      02-dropout-backward/
```

The numbers in the folder names only decide the order. The folder name without the number is the
paper's web address, so `01-dropout` becomes `/papers/dropout`.

## Add a paper (4 steps)

1. Make a folder inside the right topic, for example `13-my-paper`. Use lower-case words joined by `-`.
2. Put a `meta.json` in it. Copy this and change the values:

```json
{
	"title": "My Paper",
	"topics": [],
	"paper": {
		"title": "The full title of the paper",
		"authors": "First Author, Second Author",
		"year": 2024,
		"kind": "breakthrough",
		"summary": "One or two sentences on what the paper shows.",
		"arxivId": "2401.12345"
	}
}
```

- `kind` is `foundational` or `breakthrough`.
- `arxivId` is just the number, like `1207.0580`. No `arXiv:` and no `v2`.

3. Add one folder per coding exercise (at least one). An exercise is written like any other
   question, see `data/app_data/README.md`. In its `README.md` the top block needs:

```
---
name: research-my-paper-first-step
title: 'My Paper: The first step'
tags: [research-papers]
difficulty: Beginner
---
```

- `name` must be unique across the whole site.
- `difficulty` is `Beginner`, `Intermediate` or `Advanced`.

4. Run the check:

```
npx vitest --run processes/papers
```

If something is wrong it tells you which file to fix. That is all: the paper shows up on the next build.

## Add a new topic

Make a folder like `10-my-topic` with a `meta.json` containing a `title` and a `description`, then
add papers inside it. An empty topic is ignored until it has a paper.
