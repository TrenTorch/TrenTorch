/** Get the wrapper scaffolding component. */
export function getWrapperScaffold(): import("svelte").Component<any, any, string> | import("svelte").SvelteComponent<any, any, any>;
/**
 * Import the proper wrapper scaffolding for the current version of Svelte.
 *
 * Supports the `wrapper` option of `render` / `mount`.
 */
export function wrapperSetup(): Promise<void>;
//# sourceMappingURL=wrapper.d.ts.map