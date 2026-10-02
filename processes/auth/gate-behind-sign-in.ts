import { rememberAfterSignInDestination } from './after-sign-in-destination';
import { signInSkipped } from './preview-mode';
import { session } from './session.svelte';
import { signInPrompt } from './sign-in-prompt.svelte';

// Click handler for links into the signed-in parts of the site (Questions,
// Problem of the Day). The links stay ordinary <a href> elements so the pages
// remain public and crawlable; this only intercepts a plain click from a
// visitor who is signed out and opens the sign-in dialog instead.
export function gateBehindSignIn(event: MouseEvent): void {
	const opensElsewhere =
		event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey;
	if (event.defaultPrevented || opensElsewhere) return;

	// Session still loading: let the click through rather than guess. The
	// pages are public, so this is a nudge to sign in, not access control.
	if (session.isLoading || session.user) return;
	if (signInSkipped()) return;

	// The clicked link's own href, which the browser resolves to an absolute
	// URL even when the static build wrote it as a relative path. Keeping only
	// the path means the destination is always on this site.
	const href = (event.currentTarget as { href?: string } | null)?.href;
	if (!href) return;
	const url = new URL(href);

	event.preventDefault();
	rememberAfterSignInDestination(url.pathname + url.search);
	signInPrompt.open('browse');
}
