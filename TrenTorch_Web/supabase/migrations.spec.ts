import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { describe, it, expect } from 'vitest';

// Static regression guard for the two real production incidents this
// session: (1) a `using (true)` SELECT policy on public.profiles made
// every signed-up user's row readable by anyone, unauthenticated
// (GHSA-cfjw-7gcv-23qh); (2) a SECURITY DEFINER trigger function
// (handle_new_user) was independently callable via PostgREST's
// auto-exposed /rest/v1/rpc/ endpoint because Postgres grants EXECUTE to
// the PUBLIC pseudo-role by default. Both are fixed in the live database
// (see the two most recent migrations below); this test is what stops a
// future migration from silently reintroducing either one, since neither
// mistake produces any application-level symptom -- the app itself never
// queries the over-permissive surface.
//
// Deliberately reads the concatenation of every applied migration file
// (not just the schema's current on-disk shape) so this only proves
// what's true after the full migration history replays in order, same
// as what actually runs against a fresh database or Supabase itself.

const MIGRATIONS_DIR = join(import.meta.dirname, 'migrations');

function readAllMigrationsInOrder(): string {
	const files = readdirSync(MIGRATIONS_DIR)
		.filter((name) => name.endsWith('.sql'))
		.sort(); // filenames are Supabase-timestamp-prefixed, so lexical == chronological
	expect(files.length, 'expected at least one migration file').toBeGreaterThan(0);
	return files.map((name) => readFileSync(join(MIGRATIONS_DIR, name), 'utf8')).join('\n');
}

describe('supabase RLS/grant regressions', () => {
	const sql = readAllMigrationsInOrder();

	it('never leaves a `using (true)` policy live on public.profiles', () => {
		// The original leak, then its own fix, both exist in migration
		// history -- what matters is that the *last* policy replayed for
		// profiles' SELECT permission isn't the wide-open one. Since Postgres
		// policies are additive (not overridden by name), and the fix
		// explicitly DROPs the old policy before creating the new one, the
		// concatenated SQL containing a later `drop policy ... using (true)`
		// is exactly the signal that this was fixed, not reintroduced.
		const createdWideOpen =
			/create policy "Profiles are viewable by everyone"[\s\S]*?using \(true\)/.test(sql);
		const droppedWideOpen =
			/drop policy "Profiles are viewable by everyone" on public\.profiles/.test(sql);
		expect(
			createdWideOpen && !droppedWideOpen,
			'profiles has a live using (true) SELECT policy'
		).toBe(false);
	});

	it('the current profiles SELECT policy scopes to auth.uid() = id', () => {
		expect(sql).toMatch(
			/create policy "Users can view their own profile"[\s\S]*?using \(auth\.uid\(\) = id\)/
		);
	});

	it('handle_new_user has no live EXECUTE grant to anon, authenticated, or public', () => {
		// Same additive-history reasoning: a `revoke` after the implicit
		// default grant is what closes the hole, so its presence for every
		// role in the require-set is what this test enforces going forward.
		for (const role of ['anon', 'authenticated', 'public']) {
			const revoked = new RegExp(
				`revoke execute on function public\\.handle_new_user\\(\\) from (?:[a-z, ]*\\b)?${role}\\b`
			).test(sql);
			expect(revoked, `expected a revoke ... from ${role} on handle_new_user`).toBe(true);
		}
	});

	it('every table with row level security enabled has at least one policy defined', () => {
		const rlsEnabledTables = [
			...sql.matchAll(/alter table (public\.\w+) enable row level security/g)
		].map((m) => m[1]);
		expect(rlsEnabledTables.length).toBeGreaterThan(0);
		for (const table of rlsEnabledTables) {
			const escaped = table.replace('.', '\\.');
			const hasPolicy = new RegExp(`create policy "[^"]+"\\s*\\n?\\s*on ${escaped}`).test(sql);
			expect(hasPolicy, `${table} has RLS enabled but no policy found in migration history`).toBe(
				true
			);
		}
	});
});
