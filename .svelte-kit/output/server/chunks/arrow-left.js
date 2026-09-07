import { d as spread_props } from "./server.js";
import { t as Icon } from "./Icon.js";
//#region node_modules/@lucide/svelte/dist/icons/arrow-left.svelte
function Arrow_left($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "arrow-left",
		"size": 24,
		"node": [["path", { "d": "m12 19-7-7 7-7" }], ["path", { "d": "M19 12H5" }]]
	} }]));
}
//#endregion
export { Arrow_left as t };
