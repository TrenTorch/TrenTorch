/**
 * Render a component into the document.
 *
 * @template {import('../types.js').Component} C
 * @template {import('../types.js').Component} [W=never]
 *
 * @param {import('../types.js').ComponentImport<C>} Component - The component to render.
 * @param {import('../types.js').ComponentOptions<C>} componentOptions - Customize how Svelte renders the component.
 * @param {import('../types.js').SetupOptions<W>} setupOptions - Customize how the document and component is set up.
 * @returns {import('../types.js').RenderResult<C, W>} The rendered component.
 */
export function render<C extends import("../types.js").Component, W extends import("../types.js").Component = never>(Component: import("../types.js").ComponentImport<C>, componentOptions: import("../types.js").ComponentOptions<C>, setupOptions?: import("../types.js").SetupOptions<W>): import("../types.js").RenderResult<C, W>;
//# sourceMappingURL=render.d.ts.map