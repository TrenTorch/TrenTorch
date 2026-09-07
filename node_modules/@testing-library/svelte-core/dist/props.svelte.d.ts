/**
 * Create a shallowly reactive props object.
 *
 * This allows us to update props on `rerender` without turning the user's
 * props into a deeply reactive `$state` proxy.
 *
 * @template {Record<string, unknown>} Props
 * @param {Props} initialProps
 * @returns {[Props, (nextProps: Partial<Props>) => void]}
 */
export function createProps<Props extends Record<string, unknown>>(initialProps?: Props): [Props, (nextProps: Partial<Props>) => void];
//# sourceMappingURL=props.svelte.d.ts.map