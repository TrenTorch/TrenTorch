import { browser } from '$app/environment';
import { recordPotdAttempt } from '$processes/progress-tracking/supabase-potd-attempts-store';
import { isCurrentPotd, isUpcomingPotd } from './is-current-potd';
import { recordPotdOutcome } from './supabase-rating-store';
import { ratingStore } from './rating-store.svelte';

// A passing Submit whose attempt save or rating update still failed after the
// in-request retries (offline, Supabase down, expired session). It is kept
// here and replayed on a later visit. The database only awards a solve rating
// on the scheduled UTC day, so an entry is dropped once that day is over.
export interface PendingPotdSolve {
	userId: string;
	questionId: string;
	passedTests: number;
	totalTests: number;
}

const STORAGE_KEY = 'trentorch-pending-potd-solves';

function read(): PendingPotdSolve[] {
	if (!browser) return [];
	try {
		const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '[]');
		return Array.isArray(parsed) ? parsed : [];
	} catch {
		return [];
	}
}

function write(entries: PendingPotdSolve[]) {
	if (!browser) return;
	try {
		if (entries.length === 0) localStorage.removeItem(STORAGE_KEY);
		else localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
	} catch {
		// Storage unavailable: the retry just won't survive a reload.
	}
}

const sameSolve = (a: PendingPotdSolve, b: PendingPotdSolve) =>
	a.userId === b.userId && a.questionId === b.questionId;

export function queuePendingPotdSolve(entry: PendingPotdSolve) {
	write([...read().filter((e) => !sameSolve(e, entry)), entry]);
}

export function clearPendingPotdSolve(userId: string, questionId: string) {
	write(read().filter((e) => !(e.userId === userId && e.questionId === questionId)));
}

let flushing: Promise<void> | null = null;

// Replays this user's queued solves. Safe to call repeatedly: both RPCs are
// idempotent per (user, question), and concurrent calls share one run.
export function flushPendingPotdSolves(userId: string): Promise<void> {
	flushing ??= run(userId).finally(() => {
		flushing = null;
	});
	return flushing;
}

async function run(userId: string): Promise<void> {
	for (const entry of read().filter((e) => e.userId === userId)) {
		// Window not open yet: keep. Window closed (or not a POTD): drop.
		if (!isCurrentPotd(entry.questionId)) {
			if (!isUpcomingPotd(entry.questionId)) clearPendingPotdSolve(userId, entry.questionId);
			continue;
		}
		const saved = await recordPotdAttempt(
			entry.questionId,
			entry.passedTests,
			entry.totalTests,
			true
		);
		if (!saved.ok) continue;
		const outcome = await recordPotdOutcome(entry.questionId, 'solved');
		if (!outcome) continue;
		ratingStore.setRating(outcome.ratingAfter);
		clearPendingPotdSolve(userId, entry.questionId);
	}
}
