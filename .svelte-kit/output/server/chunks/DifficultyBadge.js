import { k as escape_html, p as stringify } from "./server.js";
import { r as Badge } from "./solved.svelte.js";
//#region platform/components/DifficultyBadge.svelte
function DifficultyBadge($$renderer, $$props) {
	let { difficulty } = $$props;
	Badge($$renderer, {
		variant: "outline",
		class: `font-mono text-xs ${stringify({
			Easy: "text-green-600 dark:text-green-400 border-green-600/30",
			Medium: "text-yellow-600 dark:text-yellow-400 border-yellow-600/30",
			Hard: "text-red-600 dark:text-red-400 border-red-600/30"
		}[difficulty])}`,
		children: ($$renderer) => {
			$$renderer.push(`<!---->${escape_html(difficulty)}`);
		},
		$$slots: { default: true }
	});
}
//#endregion
export { DifficultyBadge as t };
