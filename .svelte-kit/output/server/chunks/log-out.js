import { d as spread_props } from "./server.js";
import { t as Icon } from "./Icon.js";
//#region node_modules/@lucide/svelte/dist/icons/log-out.svelte
function Log_out($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "log-out",
		"size": 24,
		"node": [
			["path", { "d": "m16 17 5-5-5-5" }],
			["path", { "d": "M21 12H9" }],
			["path", { "d": "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" }]
		]
	} }]));
}
//#endregion
export { Log_out as t };
