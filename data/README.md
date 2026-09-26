# data/

Two folders, two different things:

- **`app_data/`** — the curriculum content itself: one `README.md` + `starter.py` + `solution.py` + `tests.py` per question, compiled by `processes/curriculum-build/build.mjs` (run it manually with `node processes/curriculum-build/build.mjs`) into `data/curriculum/generated-curriculum.json`. See [`app_data/README.md`](app_data/README.md) for the authoring format.
- **`user_data/`** — not real files, just documentation of what the app persists client-side (`localStorage`) per visitor: solved/attempted question ids, saved code, IDE layout, theme. See [`user_data/README.md`](user_data/README.md).
