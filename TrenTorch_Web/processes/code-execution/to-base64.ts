export function toBase64(str: string): string {
	try {
		return btoa(unescape(encodeURIComponent(str)));
	} catch {
		return Buffer.from(str, 'utf-8').toString('base64');
	}
}
