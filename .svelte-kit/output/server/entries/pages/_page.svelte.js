import { D as attr, k as escape_html, s as ensure_array_like } from "../../chunks/server.js";
import { t as resolve } from "../../chunks/paths.js";
import { n as LogoBadge, t as GithubIcon } from "../../chunks/GithubIcon.js";
import { t as Book_open } from "../../chunks/book-open.js";
import { t as X } from "../../chunks/x.js";
import { t as Button } from "../../chunks/Button.js";
import { t as StatTile } from "../../chunks/StatTile.js";
import { o as getProgressStats, t as curriculum } from "../../chunks/questions.js";
//#region platform/components/HowItWorks.svelte
function HowItWorks($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const STEPS = [
			{
				title: "Read the theory",
				body: "First principles, then the real math: a deep dive that builds intuition before rigor, with hints if you get stuck."
			},
			{
				title: "Implement the real signature",
				body: "The exact function torch.nn.functional actually exposes: real shapes, real defaults, no simplified stand-in."
			},
			{
				title: "Submit against hidden tests",
				body: "An exhaustive suite: edge cases, mutation tests, some checked against real offline PyTorch output. Pass everything, it's solved."
			}
		];
		$$renderer.push(`<div class="mx-auto grid max-w-4xl gap-8 text-left sm:grid-cols-3"><!--[-->`);
		const each_array = ensure_array_like(STEPS);
		for (let i = 0, $$length = each_array.length; i < $$length; i++) {
			let step = each_array[i];
			$$renderer.push(`<div><span class="font-mono text-sm font-bold text-primary">${escape_html(String(i + 1).padStart(2, "0"))}</span> <h3 class="mt-2 mb-2 font-semibold">${escape_html(step.title)}</h3> <p class="text-sm text-muted-foreground">${escape_html(step.body)}</p></div>`);
		}
		$$renderer.push(`<!--]--></div>`);
	});
}
//#endregion
//#region platform/components/Testimonials.svelte
function Testimonials($$renderer) {
	const TESTIMONIALS = [
		{
			quote: "i'm glad you're making the hard parts accessible. cuda and inference need more hands-on paths like this.",
			name: "Mena Botrous",
			handle: "@MenaBotrous11",
			url: "https://x.com/MenaBotrous11/status/2098414375866339780"
		},
		{
			quote: "I forked this project and am studying it carefully. Thank you for your jobs.",
			name: "胡林江",
			handle: "@hulj13",
			url: "https://x.com/hulj13/status/2098411277307801872"
		},
		{
			quote: "Excited for this",
			name: "Parzival",
			handle: "@0xAech",
			url: "https://x.com/0xAech/status/2098415536011096424"
		},
		{
			quote: "Honestly not a big fan of ML, but thank you for making learning accessible to everyone who are interested to learn these kind of stuff",
			name: ";::;",
			handle: "@spykedev1",
			url: "https://x.com/spykedev1/status/2099300277295657406"
		},
		{
			quote: "cool work man Must check out",
			name: "abhinav",
			handle: "@AbhinavXJ",
			url: "https://x.com/AbhinavXJ/status/2099366578248937922"
		},
		{
			quote: "Let's goo. Noice man it would help new forks",
			name: "Athrix ☄️",
			handle: "@athrix_codes",
			url: "https://x.com/athrix_codes/status/2099409710579642664"
		}
	];
	$$renderer.push(`<div class="container grid gap-4 px-4 sm:grid-cols-2 md:px-6 lg:grid-cols-3"><!--[-->`);
	const each_array = ensure_array_like(TESTIMONIALS);
	for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
		let t = each_array[$$index];
		$$renderer.push(`<a${attr("href", t.url)} target="_blank" rel="noopener noreferrer external" class="flex flex-col justify-between gap-4 rounded-md border border-border p-5 transition-colors hover:border-foreground/30 hover:bg-secondary"><p class="text-sm text-foreground">“${escape_html(t.quote)}”</p> <div class="flex items-center justify-between gap-2 text-xs text-muted-foreground"><span><span class="font-medium text-foreground">${escape_html(t.name)}</span> ${escape_html(t.handle)}</span> `);
		X($$renderer, {
			class: "size-3.5 shrink-0",
			"aria-hidden": "true"
		});
		$$renderer.push(`<!----></div></a>`);
	}
	$$renderer.push(`<!--]--></div>`);
}
//#endregion
//#region platform/routes/+page.svelte
function _page($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		const GITHUB_URL = "https://github.com/TrenTorch/TrenTorch";
		const totalQuestions = getProgressStats().total;
		const totalParts = curriculum.length;
		const FEATURES = [
			{
				title: "Real PyTorch, not a stand-in",
				body: "Functions mirror torch.nn.functional exactly: real signatures, real shape conventions, real bias=None and reduction semantics. What you implement is what the library actually does."
			},
			{
				title: "Tests that actually catch bugs",
				body: "Every Submit runs an exhaustive hidden suite: edge cases, array hygiene, targeted mutation tests, some checked against real offline PyTorch output."
			},
			{
				title: "Linear algebra to LLM post-training",
				body: `${totalQuestions} questions across ${totalParts} tracks: classical ML, deep learning foundations, transformers, vision, and production ML engineering, all built from scratch.`
			},
			{
				title: "Open source, same team",
				body: "Built by the same maintainers, under the same governance and Code of Conduct as the TrenTorch CLI itself."
			}
		];
		$$renderer.push(`<div class="svelte-1x8dnl"><section class="container flex flex-col items-center px-4 pt-24 pb-16 text-center md:px-6 svelte-1x8dnl">`);
		LogoBadge($$renderer, { class: "mb-8 size-36" });
		$$renderer.push(`<!----> <h1 class="glitch-heading mb-4 font-mono text-4xl font-bold tracking-[0.02em] sm:text-6xl svelte-1x8dnl" data-text="TrenTorch">TrenTorch</h1> <p class="mb-2 max-w-2xl text-lg text-muted-foreground svelte-1x8dnl">TrenTorch, minus the terminal.</p> <p class="mb-8 max-w-2xl text-lg font-medium svelte-1x8dnl">The same build-it-by-hand curriculum, running straight in your browser.</p> <div class="flex flex-wrap items-center justify-center gap-3 svelte-1x8dnl">`);
		Button($$renderer, {
			size: "lg",
			href: resolve("/questions"),
			children: ($$renderer) => {
				Book_open($$renderer, { class: "size-4" });
				$$renderer.push(`<!----> Questions`);
			},
			$$slots: { default: true }
		});
		$$renderer.push(`<!----> `);
		Button($$renderer, {
			size: "lg",
			variant: "outline",
			href: GITHUB_URL,
			target: "_blank",
			rel: "noopener noreferrer",
			children: ($$renderer) => {
				GithubIcon($$renderer, { class: "size-4" });
				$$renderer.push(`<!----> View on GitHub`);
			},
			$$slots: { default: true }
		});
		$$renderer.push(`<!----></div></section> <section class="container px-4 pb-16 md:px-6 svelte-1x8dnl"><div class="mx-auto grid max-w-md grid-cols-2 gap-4 svelte-1x8dnl">`);
		StatTile($$renderer, {
			label: "Questions",
			value: totalQuestions,
			tone: "positive"
		});
		$$renderer.push(`<!----> `);
		StatTile($$renderer, {
			label: "Tracks",
			value: totalParts,
			tone: "positive"
		});
		$$renderer.push(`<!----></div></section> <section class="pb-16 svelte-1x8dnl"><h2 class="mb-6 text-center font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase svelte-1x8dnl">What people are saying</h2> `);
		Testimonials($$renderer, {});
		$$renderer.push(`<!----></section> <section class="container px-4 pb-16 md:px-6 svelte-1x8dnl"><h2 class="mb-8 text-center font-mono text-xs font-semibold tracking-wider text-muted-foreground uppercase svelte-1x8dnl">How it works</h2> `);
		HowItWorks($$renderer, {});
		$$renderer.push(`<!----></section> <section class="container px-4 pb-24 md:px-6 svelte-1x8dnl"><div class="mx-auto grid max-w-4xl gap-px border bg-border sm:grid-cols-2 svelte-1x8dnl"><!--[-->`);
		const each_array = ensure_array_like(FEATURES);
		for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
			let feature = each_array[$$index];
			$$renderer.push(`<div class="bg-background p-6 svelte-1x8dnl"><h3 class="mb-2 font-mono font-semibold svelte-1x8dnl">${escape_html(feature.title)}</h3> <p class="text-sm text-muted-foreground svelte-1x8dnl">${escape_html(feature.body)}</p></div>`);
		}
		$$renderer.push(`<!--]--></div></section></div>`);
	});
}
//#endregion
export { _page as default };
