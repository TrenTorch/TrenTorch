import { D as attr, a as derived, c as head, k as escape_html, n as attr_style, p as stringify, s as ensure_array_like, t as attr_class } from "../../../chunks/server.js";
import { t as resolve } from "../../../chunks/paths.js";
import { n as Arrow_right, t as ProfileCard } from "../../../chunks/ProfileCard.js";
import { t as Log_out } from "../../../chunks/log-out.js";
import { i as session, s as signOut, t as solved } from "../../../chunks/solved.svelte.js";
import { t as Button } from "../../../chunks/Button.js";
import { t as signInPrompt } from "../../../chunks/sign-in-prompt.svelte.js";
import { t as StatTile } from "../../../chunks/StatTile.js";
import { a as getPartProgress, i as getInProgressCount, n as findQuestionBySlug, o as getProgressStats, r as getDifficultyProgress } from "../../../chunks/questions.js";
import { t as DifficultyBadge } from "../../../chunks/DifficultyBadge.js";
import { t as attempted } from "../../../chunks/attempted.svelte.js";
//#region platform/components/ContinueLearning.svelte
function ContinueLearning($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const MAX_ITEMS = 6;
		const items = derived(() => [...attempted.slugs].filter((slug) => !solved.isSolved(slug)).reverse().map((slug) => findQuestionBySlug(slug)).filter((item) => item !== void 0).slice(0, MAX_ITEMS));
		if (items().length > 0) {
			$$renderer.push(`<!--[0--><div class="space-y-1"><!--[-->`);
			const each_array = ensure_array_like(items());
			for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
				let item = each_array[$$index];
				$$renderer.push(`<a${attr("href", resolve("/ide/[id]", { id: item.question.slug }))} class="group flex items-center justify-between gap-3 rounded px-2 py-2 transition-colors hover:bg-secondary"><div class="min-w-0"><p class="truncate font-mono text-sm">${escape_html(item.question.title)}</p> <p class="truncate text-xs text-muted-foreground">${escape_html(item.partTitle)} · ${escape_html(item.trackName)}</p></div> <div class="flex shrink-0 items-center gap-2">`);
				DifficultyBadge($$renderer, { difficulty: item.question.difficulty });
				$$renderer.push(`<!----> `);
				Arrow_right($$renderer, { class: "size-4 text-muted-foreground transition-transform group-hover:translate-x-0.5" });
				$$renderer.push(`<!----></div></a>`);
			}
			$$renderer.push(`<!--]--></div>`);
		} else $$renderer.push(`<!--[-1--><p class="text-sm text-muted-foreground">Nothing in progress yet. <a${attr("href", resolve("/questions"))} class="underline hover:text-foreground">Pick a question</a> to get started.</p>`);
		$$renderer.push(`<!--]-->`);
	});
}
//#endregion
//#region platform/components/PartsChart.svelte
function PartsChart($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const rows = derived(() => getPartProgress(solved.slugs));
		$$renderer.push(`<div class="space-y-3"><!--[-->`);
		const each_array = ensure_array_like(rows());
		for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
			let row = each_array[$$index];
			const percent = row.total === 0 ? 0 : Math.round(row.solved / row.total * 100);
			$$renderer.push(`<div class="flex items-center gap-3"><span class="w-56 shrink-0 truncate font-mono text-xs text-muted-foreground"${attr("title", row.title)}>${escape_html(row.title)}</span> <div class="flex flex-1 items-center gap-2"><div class="h-4 flex-1 overflow-hidden rounded-sm bg-secondary"><div class="h-full rounded-sm bg-primary transition-all"${attr_style(`width: ${stringify(percent)}%`)}></div></div> <span class="w-14 shrink-0 text-right font-mono text-xs text-muted-foreground tabular-nums">${escape_html(row.solved)}/${escape_html(row.total)}</span></div></div>`);
		}
		$$renderer.push(`<!--]--></div>`);
	});
}
//#endregion
//#region platform/components/DifficultyChart.svelte
function DifficultyChart($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const rows = derived(() => getDifficultyProgress(solved.slugs));
		const barClass = {
			Easy: "bg-green-600 dark:bg-green-400",
			Medium: "bg-yellow-600 dark:bg-yellow-400",
			Hard: "bg-red-600 dark:bg-red-400"
		};
		$$renderer.push(`<div class="space-y-3"><!--[-->`);
		const each_array = ensure_array_like(rows());
		for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
			let row = each_array[$$index];
			const percent = row.total === 0 ? 0 : Math.round(row.solved / row.total * 100);
			$$renderer.push(`<div class="flex items-center gap-3"><span class="w-16 shrink-0 font-mono text-xs text-muted-foreground">${escape_html(row.difficulty)}</span> <div class="flex flex-1 items-center gap-2"><div class="h-4 flex-1 overflow-hidden rounded-sm bg-secondary"><div${attr_class(`h-full rounded-sm transition-all ${stringify(barClass[row.difficulty])}`)}${attr_style(`width: ${stringify(percent)}%`)}></div></div> <span class="w-14 shrink-0 text-right font-mono text-xs text-muted-foreground tabular-nums">${escape_html(row.solved)}/${escape_html(row.total)}</span></div></div>`);
		}
		$$renderer.push(`<!--]--></div>`);
	});
}
//#endregion
//#region platform/routes/account/+page.svelte
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const stats = derived(() => getProgressStats(solved.slugs));
		const percent = derived(() => stats().total === 0 ? 0 : Math.round(stats().completed / stats().total * 100));
		const inProgress = derived(() => getInProgressCount(solved.slugs, attempted.slugs));
		const notStarted = derived(() => stats().total - stats().completed - inProgress());
		head("z664cp", $$renderer, ($$renderer) => {
			$$renderer.push(`<meta name="description" content="Your TrenTorch account and progress."/>`);
		});
		$$renderer.push(`<div class="container max-w-5xl px-4 py-12 md:px-6"><div class="grid gap-6 lg:grid-cols-[320px_1fr] lg:items-start"><div class="space-y-5 rounded-md border border-border p-6">`);
		ProfileCard($$renderer, { name: "Student" });
		$$renderer.push(`<!----> <p class="text-sm text-muted-foreground">Progress is stored in this browser, not synced across devices yet.</p> <div><p class="font-mono text-4xl font-bold tabular-nums">${escape_html(percent())}%</p> <p class="mt-1 text-xs text-muted-foreground">of the curriculum solved</p></div> <div class="border-t border-border pt-4">`);
		if (session.user) {
			$$renderer.push(`<!--[0--><p class="mb-2 truncate text-sm text-muted-foreground">Signed in as <span class="font-medium text-foreground">${escape_html(session.user.email)}</span></p> `);
			Button($$renderer, {
				variant: "outline",
				size: "sm",
				onclick: signOut,
				children: ($$renderer) => {
					Log_out($$renderer, { class: "size-3.5" });
					$$renderer.push(`<!----> Sign out`);
				},
				$$slots: { default: true }
			});
			$$renderer.push(`<!---->`);
		} else {
			$$renderer.push("<!--[-1-->");
			Button($$renderer, {
				size: "sm",
				class: "w-full",
				onclick: () => signInPrompt.open(),
				children: ($$renderer) => {
					$$renderer.push(`<!---->Sign in / Sign up`);
				},
				$$slots: { default: true }
			});
		}
		$$renderer.push(`<!--]--></div></div> <div class="space-y-8"><div class="grid grid-cols-2 gap-4 sm:grid-cols-4">`);
		StatTile($$renderer, {
			label: "Solved",
			value: stats().completed,
			tone: "positive"
		});
		$$renderer.push(`<!----> `);
		StatTile($$renderer, {
			label: "In progress",
			value: inProgress()
		});
		$$renderer.push(`<!----> `);
		StatTile($$renderer, {
			label: "Not started",
			value: notStarted()
		});
		$$renderer.push(`<!----> `);
		StatTile($$renderer, {
			label: "Total questions",
			value: stats().total
		});
		$$renderer.push(`<!----></div> <div class="rounded-md border border-border p-6"><h2 class="mb-4 font-mono font-semibold">Continue where you left off</h2> `);
		ContinueLearning($$renderer, {});
		$$renderer.push(`<!----></div> <div class="rounded-md border border-border p-6"><h2 class="mb-4 font-mono font-semibold">Progress by Part</h2> `);
		PartsChart($$renderer, {});
		$$renderer.push(`<!----></div> <div class="rounded-md border border-border p-6"><h2 class="mb-4 font-mono font-semibold">Progress by difficulty</h2> `);
		DifficultyChart($$renderer, {});
		$$renderer.push(`<!----></div></div></div></div>`);
	});
}
//#endregion
export { _page as default };
