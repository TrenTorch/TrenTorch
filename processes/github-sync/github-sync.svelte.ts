import { session } from '$processes/auth/session.svelte';

export interface SolutionPayload {
	questionId: string;
	title: string;
	difficulty: string;
	tags: string[];
	description: string;
	code: string;
}

type Status = 'unknown' | 'unavailable' | 'disconnected' | 'connected';

let status = $state<Status>('unknown');
let repo = $state<string | null>(null);
let lastSyncedAt = $state<number | null>(null);
let lastError = $state<string | null>(null);
let busy = $state(false);

const authHeaders = (): Record<string, string> | null => {
	const token = session.current?.access_token;
	return token ? { authorization: `Bearer ${token}` } : null;
};

export const githubSync = {
	get status() {
		return status;
	},
	get repo() {
		return repo;
	},
	get lastSyncedAt() {
		return lastSyncedAt;
	},
	get lastError() {
		return lastError;
	},
	get busy() {
		return busy;
	}
};

export function resetGithubSync() {
	status = 'unknown';
	repo = null;
	lastSyncedAt = null;
	lastError = null;
}

// The functions only exist on the deployed site, so any failure here (the dev
// server answering 404 with HTML, a network error) means "unavailable", not an
// error the student needs to see.
export async function loadGithubStatus(): Promise<void> {
	const headers = authHeaders();
	if (!headers) return;
	try {
		const res = await fetch('/api/github/status', { headers });
		if (!res.ok) throw new Error(String(res.status));
		const body = (await res.json()) as { connected: boolean; repo?: string };
		status = body.connected ? 'connected' : 'disconnected';
		repo = body.repo ?? null;
	} catch {
		status = 'unavailable';
	}
}

export async function connectGithub(): Promise<void> {
	const headers = authHeaders();
	if (!headers || busy) return;
	busy = true;
	lastError = null;
	try {
		const res = await fetch('/api/github/start', { method: 'POST', headers });
		if (!res.ok) throw new Error(String(res.status));
		const { url } = (await res.json()) as { url: string };
		window.location.assign(url);
	} catch {
		lastError = 'Could not start the GitHub connection. Try again in a moment.';
		busy = false;
	}
}

export async function disconnectGithub(): Promise<void> {
	const headers = authHeaders();
	if (!headers || busy) return;
	busy = true;
	try {
		const res = await fetch('/api/github/disconnect', { method: 'POST', headers });
		if (res.ok) resetGithubSync();
		if (res.ok) status = 'disconnected';
	} finally {
		busy = false;
	}
}

// Fire-and-forget from the IDE after a passing Submit: never throws, and does
// nothing unless the student has connected a repo.
export async function syncSolutionToGithub(payload: SolutionPayload): Promise<void> {
	if (status !== 'connected') return;
	const headers = authHeaders();
	if (!headers) return;
	try {
		const res = await fetch('/api/github/sync', {
			method: 'POST',
			headers: { ...headers, 'content-type': 'application/json' },
			body: JSON.stringify(payload)
		});
		if (res.status === 409) {
			// Access was revoked on GitHub's side.
			status = 'disconnected';
			repo = null;
			return;
		}
		if (!res.ok) throw new Error(String(res.status));
		lastSyncedAt = Date.now();
		lastError = null;
	} catch {
		lastError = 'Last GitHub save failed. It retries on your next passing submit.';
	}
}
