import { D as attr, a as derived, c as head, k as escape_html, s as ensure_array_like } from "../../../../chunks/server.js";
import { t as resolve } from "../../../../chunks/paths.js";
import { t as Arrow_left } from "../../../../chunks/arrow-left.js";
import { t as getPartIcon } from "../../../../chunks/part-icons.js";
import { t as QuestionRow } from "../../../../chunks/QuestionRow.js";
import { t as solved } from "../../../../chunks/solved.svelte.js";
//#region platform/routes/questions/[partId]/+page.svelte
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { data } = $$props;
		const part = derived(() => data.part);
		const Icon = derived(() => getPartIcon(part().id));
		const totalQuestions = derived(() => part().tracks.reduce((sum, t) => sum + t.questions.length, 0));
		const solvedCount = derived(() => part().tracks.flatMap((t) => t.questions).filter((q) => solved.isSolved(q.slug)).length);
		head("1jbt8jg", $$renderer, ($$renderer) => {
			$$renderer.title(($$renderer) => {
				$$renderer.push(`<title>${escape_html(part().title)} | TrenTorch</title>`);
			});
		});
		$$renderer.push(`<div class="container flex flex-col gap-6 px-4 py-12 md:px-6"><div><a${attr("href", resolve("/questions"))} class="mb-4 inline-flex items-center gap-1.5 font-mono text-xs tracking-wider text-muted-foreground uppercase transition-colors hover:text-primary">`);
		Arrow_left($$renderer, { class: "size-3.5" });
		$$renderer.push(`<!----> All tracks</a> <div class="flex items-center gap-4"><span class="flex size-11 shrink-0 items-center justify-center rounded-md border border-border bg-secondary">`);
		if (Icon()) {
			$$renderer.push("<!--[-->");
			Icon()($$renderer, {
				class: "size-5 text-foreground/80",
				"aria-hidden": "true"
			});
			$$renderer.push("<!--]-->");
		} else {
			$$renderer.push("<!--[!-->");
			$$renderer.push("<!--]-->");
		}
		$$renderer.push(`</span> <div><h1 class="text-2xl font-bold">${escape_html(part().title)}</h1> <p class="text-sm text-muted-foreground">${escape_html(totalQuestions())} questions${escape_html(solvedCount() > 0 ? ` · ${solvedCount()} done` : "")}</p></div></div></div> <div class="space-y-6"><!--[-->`);
		const each_array = ensure_array_like(part().tracks);
		for (let $$index_1 = 0, $$length = each_array.length; $$index_1 < $$length; $$index_1++) {
			let track = each_array[$$index_1];
			$$renderer.push(`<section class="overflow-hidden rounded-md border border-border"><div class="flex items-center justify-between gap-3 border-b border-l-2 border-border border-l-primary bg-secondary/40 px-4 py-3"><h2 class="font-semibold">${escape_html(track.name)}</h2> <span class="text-xs text-muted-foreground">${escape_html(track.questions.length)} questions</span></div> <!--[-->`);
			const each_array_1 = ensure_array_like(track.questions);
			for (let $$index = 0, $$length = each_array_1.length; $$index < $$length; $$index++) {
				let question = each_array_1[$$index];
				QuestionRow($$renderer, { question });
			}
			$$renderer.push(`<!--]--></section>`);
		}
		$$renderer.push(`<!--]--></div></div>`);
	});
}
//#endregion
export { _page as default };
