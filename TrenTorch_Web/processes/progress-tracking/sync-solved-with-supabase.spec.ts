import { describe, it, expect, vi, beforeEach } from 'vitest';

// In-memory stand-ins for the two localStorage-backed stores and Supabase.
const local = vi.hoisted(() => ({
	solved: new Set<string>(),
	pendingRemovals: new Set<string>(),
	attempted: new Set<string>()
}));
const remote = vi.hoisted(() => ({ rows: new Set<string>(), deleteFails: false }));

vi.mock('./solved.svelte', () => ({
	solved: {
		get slugs() {
			return local.solved;
		},
		get pendingRemovals() {
			return local.pendingRemovals;
		},
		markSolvedFromRemote: (slug: string) => void local.solved.add(slug),
		clearPendingRemovals: () => local.pendingRemovals.clear(),
		clearLocal: () => {
			local.solved.clear();
			local.pendingRemovals.clear();
		}
	}
}));
vi.mock('./attempted.svelte', () => ({
	attempted: { clearLocal: () => local.attempted.clear() }
}));
vi.mock('$processes/potd/is-potd-question', () => ({ isPotdQuestion: () => false }));
vi.mock('./supabase-solved-store', () => ({
	fetchSolvedQuestions: async () => [...remote.rows].map((question_id) => ({ question_id })),
	upsertSolvedQuestions: async (_userId: string, rows: { slug: string }[]) => {
		for (const row of rows) remote.rows.add(row.slug);
	},
	deleteSolvedQuestions: async (_userId: string, slugs: string[]) => {
		if (remote.deleteFails) return false;
		for (const slug of slugs) remote.rows.delete(slug);
		return true;
	}
}));

import { syncSolvedWithSupabase } from './sync-solved-with-supabase';

function fakeStorage() {
	const data = new Map<string, string>();
	return {
		getItem: (k: string) => data.get(k) ?? null,
		setItem: (k: string, v: string) => void data.set(k, v),
		removeItem: (k: string) => void data.delete(k)
	};
}

beforeEach(() => {
	vi.stubGlobal('localStorage', fakeStorage());
	local.solved = new Set();
	local.pendingRemovals = new Set();
	local.attempted = new Set();
	remote.rows = new Set();
	remote.deleteFails = false;
});

describe('syncSolvedWithSupabase', () => {
	it('first sign-in merges both ways: progress from before signing in is kept', async () => {
		local.solved = new Set(['a']);
		remote.rows = new Set(['b']);

		await syncSolvedWithSupabase('user-1');

		expect([...local.solved].sort()).toEqual(['a', 'b']);
		expect([...remote.rows].sort()).toEqual(['a', 'b']);
	});

	it("a different account signing in on the same browser never receives the last account's solves", async () => {
		local.solved = new Set(['a-solve']);
		await syncSolvedWithSupabase('user-a');
		const accountA = new Set(remote.rows);

		// User A signs out (local progress stays), user B signs in.
		local.attempted = new Set(['a-attempt']);
		remote.rows = new Set(['b-solve']);
		await syncSolvedWithSupabase('user-b');

		expect([...remote.rows]).toEqual(['b-solve']);
		expect([...local.solved]).toEqual(['b-solve']);
		expect(local.attempted.size).toBe(0);
		expect([...accountA]).toEqual(['a-solve']);
	});

	it('the same account signing in again still merges', async () => {
		await syncSolvedWithSupabase('user-1');
		local.solved.add('solved-while-signed-out');

		await syncSolvedWithSupabase('user-1');

		expect(remote.rows.has('solved-while-signed-out')).toBe(true);
	});

	it('a question re-attempted while signed out is deleted remotely, not pulled back', async () => {
		remote.rows = new Set(['x', 'y']);
		local.pendingRemovals = new Set(['x']);

		await syncSolvedWithSupabase('user-1');

		expect([...remote.rows]).toEqual(['y']);
		expect([...local.solved]).toEqual(['y']);
		expect(local.pendingRemovals.size).toBe(0);
	});

	it('keeps the pending removal for next time when the delete fails, and still does not resurrect it', async () => {
		remote.rows = new Set(['x']);
		local.pendingRemovals = new Set(['x']);
		remote.deleteFails = true;

		await syncSolvedWithSupabase('user-1');

		expect(local.solved.has('x')).toBe(false);
		expect([...local.pendingRemovals]).toEqual(['x']);
	});
});
