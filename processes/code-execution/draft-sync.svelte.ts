/* eslint-disable svelte/prefer-svelte-reactivity -- plain Map/Set/Date used as non-reactive scratch state; only `version` is reactive */
import { session } from '$processes/auth/session.svelte';
import { CODE_KEY_PREFIX } from './code-storage-key';
import {
	fetchDraftMeta,
	fetchDraftCodes,
	upsertDrafts,
	deleteDraft,
	type RemoteDraft
} from '$processes/progress-tracking/supabase-drafts-store';

// Per-draft "last edited" time, kept beside the code so two devices can tell
// which copy is newer. Deliberately does not start with CODE_KEY_PREFIX so
// listing the code keys never picks these up.
export const CODE_META_PREFIX = 'trentorch_codemeta_';

const PUSH_DELAY_MS = 1500;

// Bumped whenever a sync writes newer remote code into localStorage, so an
// open editor can pick it up (see the IDE page).
let version = $state(0);
let pulledIds: ReadonlySet<string> = new Set();

export const draftSync = {
	get version() {
		return version;
	},
	wasPulled(contentId: string) {
		return pulledIds.has(contentId);
	}
};

const timers = new Map<string, ReturnType<typeof setTimeout>>();

function readLocalTimestamp(contentId: string): number | null {
	try {
		const raw = localStorage.getItem(`${CODE_META_PREFIX}${contentId}`);
		const value = raw ? Date.parse(raw) : NaN;
		return Number.isNaN(value) ? null : value;
	} catch {
		return null;
	}
}

export function stampLocalDraft(contentId: string): string {
	const now = new Date().toISOString();
	try {
		localStorage.setItem(`${CODE_META_PREFIX}${contentId}`, now);
	} catch {
		// Without a stamp this draft just loses ties against a remote copy.
	}
	return now;
}

export function forgetLocalDraftStamp(contentId: string) {
	try {
		localStorage.removeItem(`${CODE_META_PREFIX}${contentId}`);
	} catch {
		// Nothing to clean up if storage is unavailable.
	}
}

// Called on every editor change: waits for the student to pause typing, then
// pushes the latest code once.
export function queueDraftPush(contentId: string, code: string, updatedAt: string) {
	const userId = session.user?.id;
	if (!userId) return;
	clearTimeout(timers.get(contentId));
	timers.set(
		contentId,
		setTimeout(() => {
			timers.delete(contentId);
			void upsertDrafts(userId, [{ contentId, code, updatedAt }]);
		}, PUSH_DELAY_MS)
	);
}

export function removeRemoteDraft(contentId: string) {
	clearTimeout(timers.get(contentId));
	timers.delete(contentId);
	const userId = session.user?.id;
	if (userId) void deleteDraft(userId, contentId);
}

function readLocalDrafts(): Map<string, { code: string; ts: number | null }> {
	const out = new Map<string, { code: string; ts: number | null }>();
	try {
		for (let i = 0; i < localStorage.length; i++) {
			const key = localStorage.key(i);
			if (!key || !key.startsWith(CODE_KEY_PREFIX)) continue;
			const contentId = key.slice(CODE_KEY_PREFIX.length);
			const code = localStorage.getItem(key);
			if (code !== null) out.set(contentId, { code, ts: readLocalTimestamp(contentId) });
		}
	} catch {
		// Storage unavailable: nothing local to reconcile.
	}
	return out;
}

function localAsDraft(contentId: string, mine: { code: string; ts: number | null }): RemoteDraft {
	return {
		contentId,
		code: mine.code,
		updatedAt: mine.ts === null ? stampLocalDraft(contentId) : new Date(mine.ts).toISOString()
	};
}

// Two-way merge, newest edit wins per question. A local draft with no stamp
// (written before sync existed) is kept and pushed rather than overwritten.
// Only timestamps are compared first, so a routine re-sync downloads nothing
// unless another device actually saved something newer.
let running: Promise<void> | null = null;

export function syncDrafts(userId: string): Promise<void> {
	// Sign-in and a tab refocus can fire together: share one run.
	running ??= runSync(userId).finally(() => {
		running = null;
	});
	return running;
}

async function runSync(userId: string): Promise<void> {
	const remoteMeta = await fetchDraftMeta(userId);
	if (remoteMeta === null) return;
	const local = readLocalDrafts();
	const toPush: RemoteDraft[] = [];
	const toPull: string[] = [];

	for (const meta of remoteMeta) {
		const mine = local.get(meta.contentId);
		const remoteTs = Date.parse(meta.updatedAt);
		if (!mine || (mine.ts !== null && remoteTs > mine.ts)) toPull.push(meta.contentId);
		else if (mine.ts === null || mine.ts > remoteTs)
			toPush.push(localAsDraft(meta.contentId, mine));
		local.delete(meta.contentId);
	}
	for (const [contentId, mine] of local) toPush.push(localAsDraft(contentId, mine));

	const pulled = new Set<string>();
	if (toPull.length > 0) {
		const drafts = await fetchDraftCodes(userId, toPull);
		for (const draft of drafts ?? []) {
			const existing = readLocalDrafts().get(draft.contentId);
			// Typing that landed while the download ran wins over the older remote copy.
			if (existing && existing.ts !== null && existing.ts > Date.parse(draft.updatedAt)) continue;
			try {
				const changed = existing?.code !== draft.code;
				localStorage.setItem(`${CODE_KEY_PREFIX}${draft.contentId}`, draft.code);
				localStorage.setItem(`${CODE_META_PREFIX}${draft.contentId}`, draft.updatedAt);
				if (changed) pulled.add(draft.contentId);
			} catch {
				// Could not store it locally; the remote copy stays put.
			}
		}
	}

	await upsertDrafts(userId, toPush);
	if (pulled.size > 0) {
		pulledIds = pulled;
		version += 1;
	}
}
