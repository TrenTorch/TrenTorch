import { k as escape_html, p as stringify, t as attr_class } from "./server.js";
//#region platform/components/StatTile.svelte
function StatTile($$renderer, $$props) {
	let { label, value, tone = "neutral" } = $$props;
	$$renderer.push(`<div class="rounded-md border border-border bg-secondary/40 p-4"><p${attr_class(`font-mono text-3xl font-bold tabular-nums ${stringify({
		neutral: "text-foreground",
		positive: "text-primary"
	}[tone])}`)}>${escape_html(value)}</p> <p class="mt-1 text-xs text-muted-foreground">${escape_html(label)}</p></div>`);
}
//#endregion
export { StatTile as t };
