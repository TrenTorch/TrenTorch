import { O as clsx$1, i as bind_props, o as element, r as attributes } from "./server.js";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import "@supabase/supabase-js";
import { tv } from "tailwind-variants";
//#region platform/lib/utils.ts
function cn(...inputs) {
	return twMerge(clsx(inputs));
}
globalThis.Date;
var SvelteSet = globalThis.Set;
var SvelteMap = globalThis.Map;
globalThis.URL;
globalThis.URLSearchParams;
/**
* @param {any} _
*/
function createSubscriber(_) {
	return () => {};
}
function getSupabaseClient() {
	throw new Error("getSupabaseClient() must only be called in the browser");
}
//#endregion
//#region processes/auth/session.svelte.ts
var currentSession = null;
var isLoading = true;
var session = {
	get current() {
		return currentSession;
	},
	get user() {
		return currentSession?.user ?? null;
	},
	get isLoading() {
		return isLoading;
	}
};
function redirectTo() {
	return `${window.location.origin}/account`;
}
async function signInWithGitHub() {
	await getSupabaseClient().auth.signInWithOAuth({
		provider: "github",
		options: { redirectTo: redirectTo() }
	});
}
async function signInWithGoogle() {
	await getSupabaseClient().auth.signInWithOAuth({
		provider: "google",
		options: { redirectTo: redirectTo() }
	});
}
async function signOut() {
	await getSupabaseClient().auth.signOut();
}
//#endregion
//#region platform/components/ui/badge/badge.svelte
var badgeVariants = tv({
	base: "h-5 gap-1 rounded-4xl border border-transparent px-2 py-0.5 text-xs font-medium transition-all has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 [&>svg]:size-3! group/badge inline-flex w-fit shrink-0 items-center justify-center overflow-hidden whitespace-nowrap transition-colors focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 aria-invalid:border-destructive aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 [&>svg]:pointer-events-none",
	variants: { variant: {
		default: "bg-primary text-primary-foreground [a]:hover:bg-primary/80",
		secondary: "bg-secondary text-secondary-foreground [a]:hover:bg-secondary/80",
		destructive: "bg-destructive/10 text-destructive focus-visible:ring-destructive/20 dark:bg-destructive/20 dark:focus-visible:ring-destructive/40 [a]:hover:bg-destructive/20",
		outline: "border-border text-foreground [a]:hover:bg-muted [a]:hover:text-muted-foreground",
		ghost: "hover:bg-muted hover:text-muted-foreground dark:hover:bg-muted/50",
		link: "text-primary underline-offset-4 hover:underline"
	} },
	defaultVariants: { variant: "default" }
});
function Badge($$renderer, $$props) {
	$$renderer.component(($$renderer) => {
		let { ref = null, href, class: className, variant = "default", children, $$slots, $$events, ...restProps } = $$props;
		element($$renderer, href ? "a" : "span", () => {
			$$renderer.push(`${attributes({
				"data-slot": "badge",
				href,
				class: clsx$1(cn(badgeVariants({ variant }), className)),
				...restProps
			})}`);
		}, () => {
			children?.($$renderer);
			$$renderer.push(`<!---->`);
		});
		bind_props($$props, { ref });
	});
}
//#endregion
//#region data/potd.ts
var potdEntries = [{
	date: "2026-09-14",
	questionId: "regularized-linear-models-ridge-regression-gaussian-elimination"
}];
//#endregion
//#region processes/potd/is-potd-question.ts
function isPotdQuestion(questionId) {
	return potdEntries.some((entry) => entry.questionId === questionId);
}
//#endregion
//#region processes/progress-tracking/supabase-solved-store.ts
async function upsertSolvedQuestion(userId, slug, isPotd) {
	const { error } = await getSupabaseClient().from("solved_questions").upsert({
		user_id: userId,
		question_id: slug,
		is_potd: isPotd
	}, { onConflict: "user_id,question_id" });
	if (error) console.error("Failed to sync solved question to Supabase", error);
}
async function deleteSolvedQuestion(userId, slug) {
	const { error } = await getSupabaseClient().from("solved_questions").delete().eq("user_id", userId).eq("question_id", slug);
	if (error) console.error("Failed to delete solved question from Supabase", error);
}
function readStorage() {
	return new SvelteSet();
}
var slugs = readStorage();
var solved = {
	get slugs() {
		return slugs;
	},
	isSolved(slug) {
		return slugs.has(slug);
	},
	markSolved(slug) {
		if (slugs.has(slug)) return;
		slugs.add(slug);
		if (session.user) upsertSolvedQuestion(session.user.id, slug, isPotdQuestion(slug));
	},
	unmarkSolved(slug) {
		if (!slugs.has(slug)) return;
		slugs.delete(slug);
		if (session.user) deleteSolvedQuestion(session.user.id, slug);
	},
	markSolvedFromRemote(slug) {
		if (slugs.has(slug)) return;
		slugs.add(slug);
	}
};
//#endregion
export { signInWithGitHub as a, SvelteMap as c, cn as d, session as i, SvelteSet as l, potdEntries as n, signInWithGoogle as o, Badge as r, signOut as s, solved as t, createSubscriber as u };
