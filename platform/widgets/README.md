# Theory-tab widgets

Plain HTML + CSS + vanilla JS interactive demos (canvas + sliders), mounted
inside a question's Theory tab. No framework, no build-time dependency
beyond what the app already ships.

The Gaussian page remains the authored reference widget. The math visualizer
set is mounted automatically for each supported `math-*` curriculum id by
`GuidePane.svelte`; its shared DOM helpers live in
`platform/components/visualizers/` and its slug-to-caption catalog lives in
`math-visualizers.js`. These helpers follow the app's existing vanilla-JS
widget contract rather than introducing Svelte components into Theory
markdown.

## How a widget question is authored

1. The question's `README.md` frontmatter gets a `widget: <id>` field.
2. The Theory section's markdown embeds the widget's raw HTML markup
   directly (marked passes raw HTML blocks through unmodified), wrapped
   in a root element carrying `data-widget="<id>"`:

   ```html
   <div class="tt-widget" data-widget="gaussian-distribution">
   	<canvas id="gcanvas"></canvas>
   	<div class="controls">...</div>
   </div>
   ```

3. `<id>.js` in this folder exports `mount(root)`, where `root` is that
   `[data-widget]` element. It queries its own DOM inside `root` (never
   `document`, so two mounted widgets never collide), wires up listeners,
   and returns a cleanup function.
4. Register the id in `registry.js` so the bundler can code-split it.

The visualizer catalog is an exception to the authored-markup flow: the
Theory page creates its widget root when it sees a supported math question
id, and the shared math module creates the controls and plot. This keeps all
48 math questions visually consistent without duplicating widget markup in
dozens of READMEs.

The inference and systems-performance visualizers follow the same generated
root lifecycle for their `inf-*` and `systems-perf-*` curriculum ids. The
description tab places a live-demo callout immediately before a Constraints
section (or after the description when there is no such section); selecting
it opens Theory and scrolls to the widget. Their canvas visualizations reuse
the shared slider, stats, button, canvas, and seeded-random helpers.
The timing-decorator and loop-vs-NumPy pages are exceptions: they lazy-load
Pyodide, execute Python (and NumPy where needed), and label their measured
durations as runtime measurements rather than illustrative estimates.

The Classical ML/Data track uses a separate generated widget catalog and the
same mount/cleanup contract. Seeded toy datasets live in
`classical-ml-datasets.js`; its training and sampling demos run in plain
JavaScript. The catalog covers the 47 slugs in its brief, including planned
pages that are not yet published in the generated curriculum.

`GuidePane.svelte` handles the rest: it dynamically imports the matching
module and calls `mount()` once the Theory tab's HTML is actually in the
DOM, and calls the returned cleanup whenever the learner leaves the tab or
switches questions.

## Shared conventions

- All widget CSS is scoped under `.tt-widget` (see `widget-base.css`) so
  a widget's own class names (`.controls`, `.btnrow`, `.readout`, ...)
  never leak into the rest of the app's styles.
- `widget-base.js` has the boilerplate every widget needs: canvas
  resize-to-CSS-box handling (`observeCanvasResize`), slider binding
  (`bindRange`), and a number formatter (`fmt`).
- `components/visualizers/` provides shared slider, stats, button, canvas,
  SVG, and seeded-random helpers for the math widget family.
- `systems-visualizer-ids.js` lists the inference and systems demo slugs;
  `systems-inference-visualizers.js` supplies their interactive renderers.
- `classical-ml-visualizer-ids.js` lists the Classical ML/Data demo slugs;
  `classical-ml-visualizers.js` supplies their data-driven renderers.
- Browsers do not execute `<script>` tags inserted via `innerHTML`
  (which is how `{@html}` renders the Theory markdown), which is exactly
  why widget behavior lives in a real, dynamically-imported JS module
  instead of an inline `<script>` block in the README.
