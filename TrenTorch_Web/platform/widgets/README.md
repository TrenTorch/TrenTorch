# Theory-tab widgets

Plain HTML + CSS + vanilla JS interactive demos (canvas + sliders), mounted
inside a question's Theory tab. No framework, no build-time dependency
beyond what the app already ships.

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
- Browsers do not execute `<script>` tags inserted via `innerHTML`
  (which is how `{@html}` renders the Theory markdown), which is exactly
  why widget behavior lives in a real, dynamically-imported JS module
  instead of an inline `<script>` block in the README.
