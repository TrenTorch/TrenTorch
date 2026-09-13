// LocalStorage persistence for student code, keyed generically by whatever
// content id the current /ide/[id] route is showing -- the IDE doesn't know
// or care if that's a question or a module. Solved status itself lives in
// processes/progress-tracking/solved.svelte.ts, the same store the
// Questions page reads, so passing an IDE's hidden tests and manually
// checking a question off on /questions both land in one place.
import { CODE_KEY_PREFIX } from './code-storage-key';

export function saveUserCode(contentId: string, code: string): void {
	if (typeof window === 'undefined') return;
	try {
		localStorage.setItem(`${CODE_KEY_PREFIX}${contentId}`, code);
	} catch (e) {
		console.error('Failed to save code to localStorage', e);
	}
}
