// Copies text to the clipboard and reports whether it worked. The async
// Clipboard API is missing or rejected on insecure origins, in some embedded
// browsers and when the permission is denied, so fall back to a hidden
// textarea and execCommand before giving up.
export async function copyText(text: string): Promise<boolean> {
	if (!text) return false;
	try {
		if (navigator.clipboard?.writeText) {
			await navigator.clipboard.writeText(text);
			return true;
		}
	} catch {
		// Fall through to the legacy path.
	}
	if (typeof document === 'undefined') return false;
	const field = document.createElement('textarea');
	field.value = text;
	field.setAttribute('readonly', '');
	field.style.position = 'fixed';
	field.style.opacity = '0';
	document.body.appendChild(field);
	try {
		field.select();
		field.setSelectionRange(0, text.length);
		return document.execCommand('copy');
	} catch {
		return false;
	} finally {
		field.remove();
	}
}
