import { a as derived, c as head, k as escape_html, s as ensure_array_like } from "../../../chunks/server.js";
import { t as resolve } from "../../../chunks/paths.js";
import "../../../chunks/state.js";
import { n as Arrow_right, t as ProfileCard } from "../../../chunks/ProfileCard.js";
import { i as ProgressSummary, n as QuestionFilters, o as Calendar_check, r as ModuleSection, t as Pagination } from "../../../chunks/Pagination.js";
import { t as solved } from "../../../chunks/solved.svelte.js";
import { t as Button } from "../../../chunks/Button.js";
import { o as getProgressStats } from "../../../chunks/questions.js";
import { t as DifficultyBadge } from "../../../chunks/DifficultyBadge.js";
import "../../../chunks/curriculum-index.js";
import "../../../chunks/get-todays-potd.js";
new Intl.DateTimeFormat("en-US", {
	month: "long",
	day: "numeric",
	year: "numeric"
});
//#endregion
//#region platform/routes/potd/+page.svelte
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const stats = derived(() => getProgressStats(solved.slugs));
		const todaysProblem = derived(() => void 0);
		const todayPart = [];
		const pastPotdCurriculum = [];
		const PARTS_PER_PAGE = 4;
		let searchQuery = "";
		let solvedFilter = "all";
		let topicFilter = "all";
		let currentPage = 1;
		const allTopics = [...todayPart, ...pastPotdCurriculum].flatMap((part) => part.tracks.flatMap((track) => track.questions.flatMap((q) => q.topics))).filter((topic, i, arr) => arr.indexOf(topic) === i).sort();
		const filteredCurriculum = derived(() => {
			const query = searchQuery.trim().toLowerCase();
			return pastPotdCurriculum.map((part) => ({
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
		const totalPages = derived(() => Math.max(1, Math.ceil(filteredCurriculum().length / PARTS_PER_PAGE)));
		const pagedCurriculum = derived(() => filteredCurriculum().slice((currentPage - 1) * PARTS_PER_PAGE, currentPage * PARTS_PER_PAGE));
		function goToPage(n) {
			currentPage = Math.min(Math.max(1, n), totalPages());
			const url = new URL(window.location.href);
			url.searchParams.set("page", String(currentPage));
			history.replaceState(history.state, "", url);
		}
		let $$settled = true;
		let $$inner_renderer;
		function $$render_inner($$renderer) {
			head("hd0xv3", $$renderer, ($$renderer) => {
				$$renderer.title(($$renderer) => {
					$$renderer.push(`<title>Problem of the Day - TrenTorch</title>`);
				});
				$$renderer.push(`<meta name="description" content="A new TrenTorch curriculum question, featured every day."/>`);
			});
			$$renderer.push(`<div class="container flex flex-col gap-8 px-4 py-12 md:flex-row md:px-6"><aside class="w-full shrink-0 space-y-6 rounded-md border border-border p-4 md:sticky md:top-20 md:h-fit md:w-64">`);
			ProfileCard($$renderer, { name: "Student" });
			$$renderer.push(`<!----> `);
			ProgressSummary($$renderer, {
				completed: stats().completed,
				total: stats().total
			});
			$$renderer.push(`<!----></aside> <div class="flex-1 space-y-6"><div class="rounded-md border border-border p-5"><div class="mb-3 flex items-center gap-2 font-mono text-xs text-muted-foreground uppercase">`);
			Calendar_check($$renderer, { class: "size-4" });
			$$renderer.push(`<!----> Today's Problem</div> `);
			if (todaysProblem()) {
				$$renderer.push(`<!--[0--><div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><div class="min-w-0"><h1 class="mb-1 truncate font-mono text-xl font-bold">${escape_html(todaysProblem().question.title)}</h1> <p class="mb-2 truncate text-sm text-muted-foreground">${escape_html(todaysProblem().sectionLabel)} · ${escape_html(todaysProblem().trackLabel)}</p> `);
				DifficultyBadge($$renderer, { difficulty: todaysProblem().question.difficulty });
				$$renderer.push(`<!----></div> `);
				Button($$renderer, {
					size: "lg",
					class: "shrink-0",
					href: resolve("/ide/[id]", { id: todaysProblem().question.slug }),
					children: ($$renderer) => {
						$$renderer.push(`<!---->Try Now `);
						Arrow_right($$renderer, { class: "size-4" });
						$$renderer.push(`<!---->`);
					},
					$$slots: { default: true }
				});
				$$renderer.push(`<!----></div>`);
			} else $$renderer.push(`<!--[-1--><p class="text-sm text-muted-foreground">No problem is featured today yet, check back soon.</p>`);
			$$renderer.push(`<!--]--></div> <!--[-->`);
			const each_array = ensure_array_like(todayPart);
			for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
				let part = each_array[$$index];
				ModuleSection($$renderer, { part });
			}
			$$renderer.push(`<!--]--> `);
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
			if (filteredCurriculum().length === 0) {
				$$renderer.push(`<!--[0--><p class="py-12 text-center text-sm text-muted-foreground">`);
				if (pastPotdCurriculum.length === 0) $$renderer.push(`<!--[0-->No past Problems of the Day yet, check back soon.`);
				else $$renderer.push(`<!--[-1-->No problems match ${escape_html(searchQuery ? `"${searchQuery}"` : "these filters")}.`);
				$$renderer.push(`<!--]--></p>`);
			} else {
				$$renderer.push(`<!--[-1--><div class="space-y-3"><!--[-->`);
				const each_array_1 = ensure_array_like(pagedCurriculum());
				for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
					let part = each_array_1[$$index_1];
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
