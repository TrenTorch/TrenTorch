const enc = new TextEncoder();
const dec = new TextDecoder();

function toBase64Url(bytes: Uint8Array): string {
	let bin = '';
	for (const b of bytes) bin += String.fromCharCode(b);
	return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function fromBase64Url(text: string): Uint8Array<ArrayBuffer> {
	const padded = text
		.replace(/-/g, '+')
		.replace(/_/g, '/')
		.padEnd(Math.ceil(text.length / 4) * 4, '=');
	const bin = atob(padded);
	return Uint8Array.from(bin, (c) => c.charCodeAt(0));
}

async function hmacKey(secret: string): Promise<CryptoKey> {
	return crypto.subtle.importKey(
		'raw',
		enc.encode(secret),
		{ name: 'HMAC', hash: 'SHA-256' },
		false,
		['sign', 'verify']
	);
}

const STATE_TTL_MS = 10 * 60 * 1000;

// The OAuth state carries the user id through GitHub and back, signed so the
// callback can trust it without a server-side session.
export async function signState(userId: string, secret: string, now = Date.now()): Promise<string> {
	const payload = toBase64Url(enc.encode(JSON.stringify({ u: userId, e: now + STATE_TTL_MS })));
	const sig = await crypto.subtle.sign('HMAC', await hmacKey(secret), enc.encode(payload));
	return `${payload}.${toBase64Url(new Uint8Array(sig))}`;
}

export async function verifyState(
	state: string,
	secret: string,
	now = Date.now()
): Promise<string | null> {
	const [payload, sig] = state.split('.');
	if (!payload || !sig) return null;
	try {
		const ok = await crypto.subtle.verify(
			'HMAC',
			await hmacKey(secret),
			fromBase64Url(sig),
			enc.encode(payload)
		);
		if (!ok) return null;
		const { u, e } = JSON.parse(dec.decode(fromBase64Url(payload)));
		return typeof u === 'string' && typeof e === 'number' && e > now ? u : null;
	} catch {
		return null;
	}
}

async function aesKey(secret: string): Promise<CryptoKey> {
	const digest = await crypto.subtle.digest('SHA-256', enc.encode(`token:${secret}`));
	return crypto.subtle.importKey('raw', digest, 'AES-GCM', false, ['encrypt', 'decrypt']);
}

export async function encryptToken(token: string, secret: string): Promise<string> {
	const iv = crypto.getRandomValues(new Uint8Array(12));
	const cipher = await crypto.subtle.encrypt(
		{ name: 'AES-GCM', iv },
		await aesKey(secret),
		enc.encode(token)
	);
	return `${toBase64Url(iv)}.${toBase64Url(new Uint8Array(cipher))}`;
}

export async function decryptToken(stored: string, secret: string): Promise<string | null> {
	const [iv, cipher] = stored.split('.');
	if (!iv || !cipher) return null;
	try {
		const plain = await crypto.subtle.decrypt(
			{ name: 'AES-GCM', iv: fromBase64Url(iv) },
			await aesKey(secret),
			fromBase64Url(cipher)
		);
		return dec.decode(plain);
	} catch {
		return null;
	}
}
