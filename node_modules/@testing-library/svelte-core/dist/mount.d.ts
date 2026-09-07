/**
 * Render a Svelte component into the document.
 *
 * @template {import('../types.js').Component} C
 * @template {import('../types.js').Component} [W=never]
 *
 * @param {import('../types.js').ComponentImport<C>} Component
 * @param {import('../types.js').MountOptions<C>} options
 * @param {import('../types.js').SetupOptions<W>} [setupOptions]
 * @returns {import('../types.js').MountResult<C>}
 */
export function mount<C extends import("../types.js").Component, W extends import("../types.js").Component = never>(Component: import("../types.js").ComponentImport<C>, options: import("../types.js").MountOptions<C>, setupOptions?: import("../types.js").SetupOptions<W>): import("../types.js").MountResult<C>;
//# sourceMappingURL=mount.d.ts.map