import { CODE_KEY_PREFIX } from './code-storage-key';

export function resetUserCode(contentId: string): void {
	if (typeof window === 'undefined') return;
	try {
		localStorage.removeItem(`${CODE_KEY_PREFIX}${contentId}`);
	} catch (e) {
		console.error('Failed to reset code in localStorage', e);
	}
}
