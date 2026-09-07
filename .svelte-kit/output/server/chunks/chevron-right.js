import { d as spread_props } from "./server.js";
import { t as Icon } from "./Icon.js";
//#region node_modules/@lucide/svelte/dist/icons/chevron-left.svelte
function Chevron_left($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "chevron-left",
		"size": 24,
		"node": [["path", { "d": "m15 18-6-6 6-6" }]]
	} }]));
}
//#endregion
//#region node_modules/@lucide/svelte/dist/icons/chevron-right.svelte
function Chevron_right($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "chevron-right",
		"size": 24,
		"node": [["path", { "d": "m9 18 6-6-6-6" }]]
	} }]));
}
//#endregion
export { Chevron_left as n, Chevron_right as t };
