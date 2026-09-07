import { d as spread_props } from "./server.js";
import { t as Icon } from "./Icon.js";
//#region node_modules/@lucide/svelte/dist/icons/book-open.svelte
function Book_open($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "book-open",
		"size": 24,
		"node": [["path", { "d": "M12 5v16" }], ["path", { "d": "M20.001 19A2 2 0 0022 17V5a2 2 0 00-1.999-2L16 3.002A5 5 0 0012 5a5 5 0 00-4-2H4a2 2 0 00-2 2v12a2 2 0 001.999 2H8a5 5 0 014 2 5 5 0 014-2z" }]]
	} }]));
}
//#endregion
export { Book_open as t };
