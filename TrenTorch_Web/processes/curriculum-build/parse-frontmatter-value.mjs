/**
 * @param {string} raw
 * @returns {string | string[]}
 */
export function parseFrontmatterValue(raw) {
	const trimmed = raw.trim();
	if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
		// A flow-sequence is one level of scalars only (see parse-readme.mjs's
		// authoring-contract comment) -- the recursive call below never hits
		// this branch again, so the result is always string[], never nested.
		return /** @type {string[]} */ (
			trimmed
				.slice(1, -1)
				.split(',')
				.map((/** @type {string} */ item) => parseFrontmatterValue(item))
				.filter((/** @type {string | string[]} */ item) => item !== '')
		);
	}
	if (
		(trimmed.startsWith('"') && trimmed.endsWith('"')) ||
		(trimmed.startsWith("'") && trimmed.endsWith("'"))
	) {
		return trimmed.slice(1, -1);
	}
	return trimmed;
}
