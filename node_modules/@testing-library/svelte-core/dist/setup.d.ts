/**
 * Set up the document to render a component.
 *
 * @template {import('../types.js').Component} C
 *
 * @param {import('../types.js').ComponentOptions<C>} componentOptions - props or mount options
 * @param {import('../types.js').SetupOptions<any>} setupOptions - base element of the document to bind any queries
 * @returns {import('../types.js').SetupResult<C>}
 */
export function setup<C extends import("../types.js").Component>(componentOptions: import("../types.js").ComponentOptions<C>, setupOptions?: import("../types.js").SetupOptions<any>): import("../types.js").SetupResult<C>;
export class UnknownSvelteOptionsError extends TypeError {
    constructor(unknownOptions: any);
}
//# sourceMappingURL=setup.d.ts.map