import { CODE_KEY_PREFIX } from './code-storage-key';

export function loadUserCode(contentId: string, defaultCode: string): string {
	if (typeof window === 'undefined') return defaultCode;
	try {
		const saved = localStorage.getItem(`${CODE_KEY_PREFIX}${contentId}`);
		return saved !== null ? saved : defaultCode;
	} catch (e) {
		console.error('Failed to load code from localStorage', e);
		return defaultCode;
	}
}
