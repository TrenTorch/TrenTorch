# User Data — Storage Contract

Documentation only. There are no real files in this folder at runtime — every user's progress lives entirely client-side, in `localStorage`, in their own browser. This folder exists so the shape of that data is written down and versioned next to the curriculum content it describes, the same way `data/app_data/README.md` documents `app_data/`.

There is no backend and no account system yet: a user's data never leaves their browser, isn't synced across devices, and disappears if they clear site data. The site is fully prerendered with no server-side compute (see `svelte.config.js`'s `adapter-static` setup), so there is nowhere server-side for this data to live even if it wanted to.

## Keys

All keys are plain `localStorage.getItem`/`setItem`, read and written by the stores/modules named below. Every read is wrapped in a try/catch that falls back to an empty value — private browsing, disabled storage, or a first visit all look the same to the app: no progress yet, not an error.

### `trentorch-solved-questions`

Written by `src/lib/stores/solved.svelte.ts`. A JSON array of question ids (the `name` field from a question's `README.md` frontmatter, e.g. `"linear-regression-hypothesis-function"`) that have passed the full test suite at least once via Submit.

```json
["linear-regression-hypothesis-function", "classification-sigmoid"]
```

### `trentorch-attempted-questions`

Written by `src/lib/stores/attempted.svelte.ts`. Same shape as above — a JSON array of question ids — but marks "has been opened and run/submitted at least once, not necessarily passed." A question can be attempted without being solved; Re-attempt (in the IDE header) clears a question out of `trentorch-solved-questions` but leaves it in this one.

```json
["linear-regression-hypothesis-function", "linear-regression-mse-loss"]
```

### `trentorch-code:<questionId>`

Written by `src/lib/runtime/storage.ts` (`CODE_KEY_PREFIX`). One key per question, holding the student's current editor contents as a plain string (not JSON) — whatever they last typed, restored the next time they open that question. Reset (in the IDE header) removes this key, falling back to the question's `starterCode`.

### `trentorch-ide-layout`

Written by `src/lib/runtime/storage.ts` (`LAYOUT_KEY`). One JSON object, shared across every question, holding the IDE's pane-split state (sizes/collapsed panes) so it doesn't reset every time a student switches questions.

### `theme`

Written by `src/lib/components/ModeToggle.svelte`. Plain string, `"dark"` or `"light"` — the whole site's theme choice, not question-specific.

## Adding a new persisted field

Add the key here first (name, shape, which module owns it, what "empty" means), then implement it — this file is the contract a future backend migration reads, not an afterthought written after the fact.
