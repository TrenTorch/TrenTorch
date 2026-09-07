/** @import { Context, Visitor, Visitors } from './types.js' */

/**
 * @template {{ type: string }} T
 * @template {Record<string, any> | null} U
 * @param {T} node
 * @param {U} state
 * @param {Visitors<T, U>} visitors
 */
export function walk(node, state, visitors) {
	const universal = visitors._;

	let stopped = false;

	const stop = () => {
		stopped = true;
	};

	/**
	 * @param {T} node
	 * @param {T[]} path
	 * @param {U} state
	 * @returns {T | undefined}
	 */
	function visit_children(node, path, state) {
		/** @type {Record<string, any> | null} lazily initialized for performance reasons */
		let mutations = null;

		path.push(node);
		for (const key in node) {
			if (
				key === 'type' ||
				// avoid manipulating the prototype
				key === '__proto__'
			) {
				continue;
			}

			const child_node = node[key];
			if (child_node && typeof child_node === 'object') {
				if (Array.isArray(child_node)) {
					/** @type {T[] | null} lazily cloned on first mutation */
					let mutated_array = null;
					const len = child_node.length;

					for (let i = 0; i < len; i++) {
						const node = child_node[i];
						if (node && typeof node === 'object') {
							const result = visit(node, path, state);
							if (result) {
								(mutated_array ??= child_node.slice())[i] = result;
							}
						}
					}

					if (mutated_array) {
						(mutations ??= {})[key] = mutated_array;
					}
				} else {
					const result = visit(/** @type {T} */ (child_node), path, state);

					// @ts-ignore
					if (result) {
						(mutations ??= {})[key] = result;
					}
				}
			}
		}
		path.pop();

		if (mutations) {
			return apply_mutations(node, mutations);
		}
	}

	/**
	 * @param {T} node
	 * @param {T[]} path
	 * @param {U} state
	 * @returns {T | undefined}
	 */
	function visit(node, path, state) {
		// Don't return the node here or it could lead to false-positive mutation detection
		if (stopped) return;
		if (!node.type) return;

		const visitor = /** @type {Visitor<T, U, T> | undefined} */ (
			visitors[/** @type {T['type']} */ (node.type)]
		);

		// nothing will run for this node, so walk its children without building a context
		if (!universal && !visitor) {
			return visit_children(node, path, state);
		}

		/** @type {T | void} */
		let result;

		/** @type {T | undefined} */
		let next_result;

		/** @type {Context<T, U>['next']} */
		const next = (next_state = state) =>
			(next_result = visit_children(node, path, next_state));

		/** @type {Context<T, U>['visit']} */
		const visit_node = (next_node, next_state = state) => {
			path.push(node);
			const result = visit(next_node, path, next_state) ?? next_node;
			path.pop();
			return result;
		};

		if (universal) {
			/** @type {T | void} */
			let inner_result;

			result = universal(node, {
				// Don't spread for performance reasons
				path,
				state,
				/** @param {U} next_state */
				next: (next_state = state) => {
					state = next_state; // make it the default for subsequent specialised visitors

					inner_result = visitor
						? visitor(node, {
								path,
								state: next_state,
								next,
								stop,
								visit: visit_node
							})
						: next(next_state);

					return inner_result;
				},
				stop,
				visit: visit_node
			});

			// @ts-expect-error TypeScript doesn't understand that `context.next(...)` is called immediately
			if (!result && inner_result) {
				result = inner_result;
			}
		} else {
			// the early return above guarantees `visitor` exists here
			result = /** @type {Visitor<T, U, T>} */ (visitor)(node, {
				path,
				state,
				next,
				stop,
				visit: visit_node
			});
		}

		if (!result && next_result) {
			result = next_result;
		}

		if (result) {
			return result;
		}
	}

	return visit(node, [], state) ?? node;
}

/**
 * @template {Record<string, any>} T
 * @param {T} node
 * @param {Record<string, any>} mutations
 * @returns {T}
 */
function apply_mutations(node, mutations) {
	/** @type {Record<string, any>} */
	const obj = {};

	const descriptors = Object.getOwnPropertyDescriptors(node);

	for (const key in descriptors) {
		Object.defineProperty(obj, key, descriptors[key]);
	}

	for (const key in mutations) {
		obj[key] = mutations[key];
	}

	return /** @type {T} */ (obj);
}
