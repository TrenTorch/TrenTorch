import { d as spread_props } from "./server.js";
import { t as Icon } from "./Icon.js";
//#region node_modules/@lucide/svelte/dist/icons/x.svelte
function X($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "x",
		"size": 24,
		"node": [["path", { "d": "M18 6 6 18" }], ["path", { "d": "m6 6 12 12" }]]
	} }]));
}
//#endregion
export { X as t };
