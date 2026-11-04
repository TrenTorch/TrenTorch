import { browser } from '$app/environment';

// What the student last opened, per area, so the green dot on a page can take them straight back to it:
// the last question opened in a module / the problemset / the DSA sheet, and the last paper read. It is a
// pointer, not progress: whether the question is still unfinished is read from solved.svelte.ts.
export type RecentArea = 'module' | 'problemset' | 'dsa' | 'paper';

const STORAGE_KEY = 'trentorch_recent';

function readStorage(): Partial<Record<RecentArea, string>> {
	if (!browser) return {};
	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		const parsed: unknown = raw ? JSON.parse(raw) : {};
		return parsed && typeof parsed === 'object'
			? (parsed as Partial<Record<RecentArea, string>>)
			: {};
	} catch {
		return {};
	}
}

let latest = $state<Partial<Record<RecentArea, string>>>(readStorage());

export const recent = {
	get(area: RecentArea): string | undefined {
		return latest[area];
	},
	note(area: RecentArea, slug: string) {
		if (latest[area] === slug) return;
		latest = { ...latest, [area]: slug };
		if (!browser) return;
		try {
			localStorage.setItem(STORAGE_KEY, JSON.stringify(latest));
		} catch {
			// The dot just won't have anywhere to go next visit.
		}
	}
};
