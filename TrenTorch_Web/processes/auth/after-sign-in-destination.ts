// Where a visitor was headed when a click sent them to sign in first. Held in
// sessionStorage because OAuth sign-in leaves the page and comes back to
// /account, so in-memory state would be lost; the root layout reads it back
// once a session exists and sends them on.
const KEY = 'trentorch-after-sign-in';

export function rememberAfterSignInDestination(path: string): void {
	try {
		sessionStorage.setItem(KEY, path);
	} catch {
		// Storage blocked: after signing in they land on /account instead.
	}
}

export function clearAfterSignInDestination(): void {
	try {
		sessionStorage.removeItem(KEY);
	} catch {
		// Nothing to clear if storage is unavailable.
	}
}

// Returns the remembered path once and forgets it. Only same-site absolute
// paths are accepted, so a tampered value cannot send someone off-site.
export function takeAfterSignInDestination(): string | null {
	try {
		const value = sessionStorage.getItem(KEY);
		if (value === null) return null;
		sessionStorage.removeItem(KEY);
		const sameSite = value.startsWith('/') && !value.startsWith('//') && !value.includes('\\');
		return sameSite ? value : null;
	} catch {
		return null;
	}
}
