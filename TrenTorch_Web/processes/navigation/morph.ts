import { goto } from '$app/navigation';
import { resolve } from '$app/paths';

// "Minimise": a page folds into the thing on the home page that stands for it (its card, the preview window,
// or the capsule under it), or a tab in the navbar. It is a View Transition: the page's header (the element marked
// `data-minimise`) scales down onto the target while the home page sits underneath, and only then fades. The root layout runs it (see onNavigate there); this is the
// part a window's dot calls. Without View Transitions, or with reduced motion, it is just the navigation.

export const HOME_COLLAPSED_KEY = 'trentorch_home_preview_collapsed';

/** What the page folds into: a `data-morph` value on the home page. */
export type MorphTarget =
	`tab:${string}` | 'card-dsa' | 'card-paper' | 'preview-window' | 'preview-pill';

interface Pending {
	target: MorphTarget;
	/** Whether the home page's preview will open folded, so it can start that way rather than animate to it. */
	homeCollapsed: boolean;
}

let pending: Pending | null = null;

export const pendingMorph = () => pending;
export const clearMorph = () => (pending = null);

export function readHomeCollapsed(): boolean {
	try {
		return localStorage.getItem(HOME_COLLAPSED_KEY) === '1';
	} catch {
		return false;
	}
}

/** Go home, folding into `target` on the way; with none it is a plain navigation. */
export async function minimiseTo(target?: MorphTarget): Promise<void> {
	pending = target ? { target, homeCollapsed: readHomeCollapsed() } : null;
	try {
		await goto(resolve('/'));
	} finally {
		clearMorph();
	}
}
