import "./server.js";
import { l as SvelteSet } from "./solved.svelte.js";
function readStorage() {
	return new SvelteSet();
}
var slugs = readStorage();
var attempted = {
	get slugs() {
		return slugs;
	},
	isAttempted(slug) {
		return slugs.has(slug);
	},
	markAttempted(slug) {
		if (slugs.has(slug)) return;
		slugs.add(slug);
	},
	unmarkAttempted(slug) {
		if (!slugs.has(slug)) return;
		slugs.delete(slug);
	}
};
//#endregion
export { attempted as t };
