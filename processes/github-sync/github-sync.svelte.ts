/* eslint-disable svelte/prefer-svelte-reactivity -- inFlight/queued are plain bookkeeping, never read by the UI */
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

const REQUEST_TIMEOUT_MS = 15_000;

let status = $state<Status>('unknown');
let repo = $state<string | null>(null);
let lastSyncedAt = $state<number | null>(null);
let lastError = $state<string | null>(null);
let busy = $state(false);

let statusLoad: Promise<void> | null = null;
// Questions with a save in flight, plus the newest payload that arrived
// meanwhile, so a double Submit never races two commits for the same files.
const inFlight = new Set<string>();
const queued = new Map<string, SolutionPayload>();

const authHeaders = (): Record<string, string> | null => {
	const token = session.current?.access_token;
	return token ? { authorization: `Bearer ${token}` } : null;
};

const request = (path: string, init: RequestInit) =>
	fetch(path, { ...init, signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS) });

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
	statusLoad = null;
	queued.clear();
}

// The functions only exist on the deployed site, so any failure here (the dev
// server answering 404 with HTML, a network error, a timeout) means
// "unavailable", not an error the student needs to see.
export function loadGithubStatus(): Promise<void> {
	if (statusLoad) return statusLoad;
	const headers = authHeaders();
	if (!headers) return Promise.resolve();
	statusLoad = (async () => {
		try {
			const res = await request('/api/github/status', { headers });
			if (!res.ok) throw new Error(String(res.status));
			const body = (await res.json()) as { connected: boolean; repo?: string };
			status = body.connected ? 'connected' : 'disconnected';
			repo = body.repo ?? null;
		} catch {
			status = 'unavailable';
		} finally {
			statusLoad = null;
		}
	})();
	return statusLoad;
}

// Right after returning from GitHub the connection can take a moment to be
// visible everywhere (the token store is eventually consistent), so a status
// read straight after the redirect may still say "disconnected".
export async function confirmFreshConnection(): Promise<void> {
	for (let attempt = 0; attempt < 4; attempt++) {
		await loadGithubStatus();
		if (githubSync.status === 'connected') return;
		await new Promise((resolve) => setTimeout(resolve, 1500));
	}
}

export async function connectGithub(): Promise<void> {
	const headers = authHeaders();
	if (!headers || busy) return;
	busy = true;
	lastError = null;
	try {
		const res = await request('/api/github/start', { method: 'POST', headers });
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
	lastError = null;
	try {
		const res = await request('/api/github/disconnect', { method: 'POST', headers });
		if (!res.ok) throw new Error(String(res.status));
		resetGithubSync();
		status = 'disconnected';
	} catch {
		lastError = 'Could not disconnect right now. Try again in a moment.';
	} finally {
		busy = false;
	}
}

async function pushOnce(payload: SolutionPayload, headers: Record<string, string>) {
	try {
		const res = await request('/api/github/sync', {
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

// Fire-and-forget from the IDE after a passing Submit: never throws, and does
// nothing unless the student has connected a repo. If the connection status
// has not loaded yet (a fast Submit on a fresh page) it waits for it, and a
// status that failed to load earlier is given one more chance.
export async function syncSolutionToGithub(payload: SolutionPayload): Promise<void> {
	if (!authHeaders()) return;
	if (status === 'unknown' || status === 'unavailable') await loadGithubStatus();
	if (status !== 'connected') return;

	if (inFlight.has(payload.questionId)) {
		queued.set(payload.questionId, payload);
		return;
	}
	inFlight.add(payload.questionId);
	try {
		let next: SolutionPayload | undefined = payload;
		while (next) {
			// Token may have refreshed or expired while a previous push ran.
			const headers = authHeaders();
			if (!headers) return;
			await pushOnce(next, headers);
			next = queued.get(payload.questionId);
			queued.delete(payload.questionId);
		}
	} finally {
		inFlight.delete(payload.questionId);
	}
}
