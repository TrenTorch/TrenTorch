import { D as attr, a as derived, d as spread_props, k as escape_html, t as attr_class } from "./server.js";
import { t as resolve } from "./paths.js";
import "./state.js";
import { t as Icon } from "./Icon.js";
import { t as solved } from "./solved.svelte.js";
import { t as DifficultyBadge } from "./DifficultyBadge.js";
import { t as attempted } from "./attempted.svelte.js";
//#region node_modules/@lucide/svelte/dist/icons/check.svelte
function Check($$renderer, $$props) {
	let { $$slots, $$events, ...props } = $$props;
	Icon($$renderer, spread_props([props, { icon: {
		"name": "check",
		"size": 24,
		"node": [["path", { "d": "M20 6 9 17l-5-5" }]]
	} }]));
}
//#endregion
//#region platform/components/QuestionRow.svelte
function QuestionRow($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { question } = $$props;
		const isSolved = derived(() => solved.isSolved(question.slug));
		const isAttempted = derived(() => !isSolved() && attempted.isAttempted(question.slug));
		const currentQuestionsPage = derived(() => null);
		const ideHref = derived(() => currentQuestionsPage() ? resolve(`/ide/[id]?from=${currentQuestionsPage()}`, { id: question.slug }) : resolve("/ide/[id]", { id: question.slug }));
		$$renderer.push(`<div class="flex items-center gap-3 border-b border-border px-3 py-2 text-sm transition-colors last:border-0 hover:bg-secondary"><div${attr_class(`flex size-4 shrink-0 items-center justify-center rounded-[4px] border ${isSolved() ? "border-primary bg-primary text-primary-foreground" : "border-input"}`)} role="img"${attr("aria-label", isSolved() ? `'${question.title}' is solved` : `'${question.title}' is not solved yet`)}${attr("title", isSolved() ? "Solved: passed every test on Submit" : "Not solved yet -- open the question and Submit passing code to earn this")}>`);
		if (isSolved()) {
			$$renderer.push("<!--[0-->");
			Check($$renderer, { class: "size-3.5" });
		} else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--></div> <a${attr("href", ideHref())} class="flex flex-1 items-center justify-between gap-2"><span${attr_class(`flex items-center gap-2 ${isSolved() ? "text-muted-foreground line-through" : ""}`)}>${escape_html(question.title)} `);
		if (isAttempted()) $$renderer.push(`<!--[0--><span class="inline-flex items-center rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 font-mono text-[10px] leading-none text-amber-600 dark:text-amber-400" title="You've submitted an attempt at this question">Attempted</span>`);
		else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--></span> `);
		DifficultyBadge($$renderer, { difficulty: question.difficulty });
		$$renderer.push(`<!----></a></div>`);
	});
}
//#endregion
export { Check as n, QuestionRow as t };
