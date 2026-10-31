import { beforeEach, describe, expect, it, vi } from 'vitest';

const store: Record<string, string> = {};
vi.stubGlobal('localStorage', {
	getItem: (k: string) => store[k] ?? null,
	setItem: (k: string, v: string) => (store[k] = v),
	removeItem: (k: string) => delete store[k]
});
vi.mock('$app/environment', () => ({ browser: true }));

const recordPotdAttempt = vi.fn();
const recordPotdOutcome = vi.fn();
const setRating = vi.fn();
let current = true;
let upcoming = false;
vi.mock('$processes/progress-tracking/supabase-potd-attempts-store', () => ({
	recordPotdAttempt: (...a: unknown[]) => recordPotdAttempt(...a)
}));
vi.mock('./supabase-rating-store', () => ({
	recordPotdOutcome: (...a: unknown[]) => recordPotdOutcome(...a)
}));
vi.mock('./rating-store.svelte', () => ({
	ratingStore: { setRating: (r: number) => setRating(r) }
}));
vi.mock('./is-current-potd', () => ({
	isCurrentPotd: () => current,
	isUpcomingPotd: () => upcoming
}));

import { flushPendingPotdSolves, queuePendingPotdSolve } from './pending-potd-solves';

const entry = { userId: 'u1', questionId: 'q1', passedTests: 6, totalTests: 6 };
const pendingCount = () => JSON.parse(store['trentorch-pending-potd-solves'] ?? '[]').length;

beforeEach(() => {
	for (const k of Object.keys(store)) delete store[k];
	recordPotdAttempt.mockReset().mockResolvedValue({ ok: true });
	recordPotdOutcome
		.mockReset()
		.mockResolvedValue({ ratingAfter: 900, delta: 40, alreadyRecorded: false });
	setRating.mockReset();
	current = true;
	upcoming = false;
});

describe('flushPendingPotdSolves', () => {
	it('replays a queued solve, applies the rating and clears it', async () => {
		queuePendingPotdSolve(entry);
		queuePendingPotdSolve(entry); // no duplicate
		expect(pendingCount()).toBe(1);
		await flushPendingPotdSolves('u1');
		expect(recordPotdAttempt).toHaveBeenCalledWith('q1', 6, 6, true);
		expect(setRating).toHaveBeenCalledWith(900);
		expect(pendingCount()).toBe(0);
	});

	it('keeps the entry when the save or the rating still fails', async () => {
		queuePendingPotdSolve(entry);
		recordPotdAttempt.mockResolvedValueOnce({ ok: false, code: null });
		await flushPendingPotdSolves('u1');
		expect(pendingCount()).toBe(1);
		recordPotdOutcome.mockResolvedValueOnce(null);
		await flushPendingPotdSolves('u1');
		expect(pendingCount()).toBe(1);
	});

	it('drops the entry once the POTD day has passed, keeps it before it opens', async () => {
		queuePendingPotdSolve(entry);
		current = false;
		upcoming = true;
		await flushPendingPotdSolves('u1');
		expect(pendingCount()).toBe(1);
		upcoming = false;
		await flushPendingPotdSolves('u1');
		expect(pendingCount()).toBe(0);
		expect(recordPotdAttempt).not.toHaveBeenCalled();
	});

	it("ignores other users' entries", async () => {
		queuePendingPotdSolve({ ...entry, userId: 'u2' });
		await flushPendingPotdSolves('u1');
		expect(recordPotdAttempt).not.toHaveBeenCalled();
		expect(pendingCount()).toBe(1);
	});
});
