import { D as attr, a as derived, c as head, k as escape_html, s as ensure_array_like, t as attr_class } from "../../../chunks/server.js";
import { t as resolve } from "../../../chunks/paths.js";
import "../../../chunks/state.js";
import { n as Arrow_right, t as ProfileCard } from "../../../chunks/ProfileCard.js";
import { t as getPartIcon } from "../../../chunks/part-icons.js";
import { a as Progress, i as ProgressSummary, n as QuestionFilters, o as Calendar_check, r as ModuleSection, t as Pagination } from "../../../chunks/Pagination.js";
import { t as Chevron_right } from "../../../chunks/chevron-right.js";
import { t as solved } from "../../../chunks/solved.svelte.js";
import { t as Button } from "../../../chunks/Button.js";
import { a as getPartProgress, o as getProgressStats, t as curriculum } from "../../../chunks/questions.js";
//#region platform/components/PartCard.svelte
function PartCard($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { id, title, icon: Icon, questionCount, solved, total } = $$props;
		const inProgress = derived(() => solved > 0 && solved < total);
		$$renderer.push(`<a${attr("href", resolve("/questions/[partId]", { partId: id }))}${attr_class(`group flex items-center gap-4 rounded-md border px-5 py-4 transition-colors ${inProgress() ? "border-primary/60" : "border-border hover:border-foreground/30"}`)}><span class="flex size-10 shrink-0 items-center justify-center rounded-md border border-border bg-secondary">`);
		if (Icon) {
			$$renderer.push("<!--[-->");
			Icon($$renderer, {
				class: "size-4.5 text-foreground/80",
				"aria-hidden": "true"
			});
			$$renderer.push("<!--]-->");
		} else {
			$$renderer.push("<!--[!-->");
			$$renderer.push("<!--]-->");
		}
		$$renderer.push(`</span> <span class="min-w-0 flex-1"><span class="block font-semibold">${escape_html(title)}</span> <span class="block text-xs text-muted-foreground">${escape_html(questionCount)} question${escape_html(questionCount === 1 ? "" : "s")} `);
		if (solved > 0) $$renderer.push(`<!--[0-->· ${escape_html(solved)} done`);
		else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--></span> `);
		if (inProgress()) {
			$$renderer.push("<!--[0-->");
			Progress($$renderer, {
				value: solved,
				max: total,
				class: "mt-2 h-1 max-w-52"
			});
		} else $$renderer.push("<!--[-1-->");
		$$renderer.push(`<!--]--></span> `);
		Arrow_right($$renderer, {
			class: "size-4 shrink-0 text-muted-foreground transition-transform group-hover:translate-x-0.5 group-hover:text-primary",
			"aria-hidden": "true"
		});
		$$renderer.push(`<!----></a>`);
	});
}
//#endregion
//#region platform/routes/questions/+page.svelte
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const stats = derived(() => getProgressStats(solved.slugs));
		const partProgress = derived(() => getPartProgress(solved.slugs));
		const PARTS_PER_PAGE = 4;
		const CARDS_PER_PAGE = 6;
		let searchQuery = "";
		let solvedFilter = "all";
		let topicFilter = "all";
		const isFiltering = derived(() => searchQuery.trim() !== "" || solvedFilter !== "all" || topicFilter !== "all");
		let currentPage = 1;
		const allTopics = curriculum.flatMap((part) => part.tracks.flatMap((track) => track.questions.flatMap((q) => q.topics))).filter((topic, i, arr) => arr.indexOf(topic) === i).sort();
		const filteredCurriculum = derived(() => {
			const query = searchQuery.trim().toLowerCase();
			return curriculum.map((part) => ({
				...part,
				tracks: part.tracks.map((track) => ({
					...track,
					questions: track.questions.filter((question) => {
						if (query && !question.title.toLowerCase().includes(query)) return false;
						if (solvedFilter === "solved" && !solved.isSolved(question.slug)) return false;
						if (solvedFilter === "unsolved" && solved.isSolved(question.slug)) return false;
						if (topicFilter !== "all" && !question.topics.includes(topicFilter)) return false;
						return true;
					})
				})).filter((track) => track.questions.length > 0)
			})).filter((part) => part.tracks.length > 0);
		});
		const totalPages = derived(() => isFiltering() ? Math.max(1, Math.ceil(filteredCurriculum().length / PARTS_PER_PAGE)) : Math.max(1, Math.ceil(curriculum.length / CARDS_PER_PAGE)));
		const pagedCurriculum = derived(() => filteredCurriculum().slice((currentPage - 1) * PARTS_PER_PAGE, currentPage * PARTS_PER_PAGE));
		const pagedParts = derived(() => curriculum.slice((currentPage - 1) * CARDS_PER_PAGE, currentPage * CARDS_PER_PAGE));
		function goToPage(n) {
			currentPage = Math.min(Math.max(1, n), totalPages());
			const url = new URL(window.location.href);
			url.searchParams.set("page", String(currentPage));
			history.replaceState(history.state, "", url);
		}
		let $$settled = true;
		let $$inner_renderer;
		function $$render_inner($$renderer) {
			head("ji57j7", $$renderer, ($$renderer) => {
				$$renderer.push(`<meta name="description" content="Every TrenTorch curriculum question, in one place."/>`);
			});
			$$renderer.push(`<div class="container flex flex-col gap-8 px-4 py-12 md:flex-row md:px-6"><aside class="w-full shrink-0 space-y-6 rounded-md border border-border p-4 md:sticky md:top-20 md:h-fit md:w-64">`);
			ProfileCard($$renderer, { name: "Student" });
			$$renderer.push(`<!----> `);
			ProgressSummary($$renderer, {
				completed: stats().completed,
				total: stats().total
			});
			$$renderer.push(`<!----></aside> <div class="flex-1 space-y-8"><div class="flex flex-col items-start justify-between gap-4 rounded-md border border-border bg-secondary/30 p-5 sm:flex-row sm:items-center"><div class="flex items-center gap-3">`);
			Calendar_check($$renderer, {
				class: "size-6 shrink-0 text-muted-foreground",
				"aria-hidden": "true"
			});
			$$renderer.push(`<!----> <div><h2 class="font-semibold">Problems of the Day</h2> <p class="text-sm text-muted-foreground">A new featured question, every day.</p></div></div> `);
			Button($$renderer, {
				href: resolve("/potd"),
				class: "shrink-0",
				children: ($$renderer) => {
					$$renderer.push(`<!---->Try Now `);
					Arrow_right($$renderer, { class: "size-4" });
					$$renderer.push(`<!---->`);
				},
				$$slots: { default: true }
			});
			$$renderer.push(`<!----></div> <div><p class="mb-1 font-mono text-xs tracking-wider text-muted-foreground uppercase">Questions `);
			Chevron_right($$renderer, { class: "inline size-3" });
			$$renderer.push(`<!----> ${escape_html(curriculum.length)} tracks `);
			if (stats().completed > 0) $$renderer.push(`<!--[0--><span class="text-primary">· ${escape_html(stats().completed)}/${escape_html(stats().total)} solved</span>`);
			else $$renderer.push("<!--[-1-->");
			$$renderer.push(`<!--]--></p> <h1 class="text-2xl font-bold">Pick a track</h1></div> `);
			QuestionFilters($$renderer, {
				topics: allTopics,
				get searchQuery() {
					return searchQuery;
				},
				set searchQuery($$value) {
					searchQuery = $$value;
					$$settled = false;
				},
				get solvedFilter() {
					return solvedFilter;
				},
				set solvedFilter($$value) {
					solvedFilter = $$value;
					$$settled = false;
				},
				get topicFilter() {
					return topicFilter;
				},
				set topicFilter($$value) {
					topicFilter = $$value;
					$$settled = false;
				}
			});
			$$renderer.push(`<!----> `);
			if (isFiltering()) {
				$$renderer.push("<!--[0-->");
				if (filteredCurriculum().length === 0) $$renderer.push(`<!--[0--><p class="py-12 text-center text-sm text-muted-foreground">No questions match ${escape_html(searchQuery ? `"${searchQuery}"` : "these filters")}.</p>`);
				else {
					$$renderer.push(`<!--[-1--><div class="space-y-3"><!--[-->`);
					const each_array = ensure_array_like(pagedCurriculum());
					for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
						let part = each_array[$$index];
						ModuleSection($$renderer, { part });
					}
					$$renderer.push(`<!--]--></div> `);
					Pagination($$renderer, {
						currentPage,
						totalPages: totalPages(),
						onPageChange: goToPage
					});
					$$renderer.push(`<!---->`);
				}
				$$renderer.push(`<!--]-->`);
			} else {
				$$renderer.push(`<!--[-1--><div class="grid gap-3"><!--[-->`);
				const each_array_1 = ensure_array_like(pagedParts());
				for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
					let part = each_array_1[$$index_1];
					const progress = partProgress().find((p) => p.id === part.id);
					PartCard($$renderer, {
						id: part.id,
						title: part.title,
						icon: getPartIcon(part.id),
						questionCount: part.tracks.reduce((sum, t) => sum + t.questions.length, 0),
						solved: progress?.solved ?? 0,
						total: progress?.total ?? 0
					});
				}
				$$renderer.push(`<!--]--></div> `);
				Pagination($$renderer, {
					currentPage,
					totalPages: totalPages(),
					onPageChange: goToPage
				});
				$$renderer.push(`<!---->`);
			}
			$$renderer.push(`<!--]--></div></div>`);
		}
		do {
			$$settled = true;
			$$inner_renderer = $$renderer.copy();
			$$render_inner($$inner_renderer);
		} while (!$$settled);
		$$renderer.subsume($$inner_renderer);
	});
}
//#endregion
export { _page as default };
