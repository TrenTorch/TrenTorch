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
const DISCUSSION_MIGRATION = join(MIGRATIONS_DIR, '20260928135000_create_potd_discussion.sql');
const DISCUSSION_RULES_MIGRATION = join(
	MIGRATIONS_DIR,
	'20260928155000_tighten_potd_discussion_rules.sql'
);

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

	it('POTD discussion tables are protected by RLS policies without wide-open access', () => {
		for (const table of ['potd_discussion_comments', 'potd_comment_votes']) {
			expect(sql, `${table} must enable row level security`).toMatch(
				new RegExp(`alter table public\\.${table} enable row level security`)
			);

			const policies = [
				...sql.matchAll(new RegExp(`create policy "[^"]+"\\s+on public\\.${table}[\\s\\S]*?;`, 'g'))
			].map((match) => match[0]);
			expect(policies.length, `${table} must have RLS policies`).toBeGreaterThan(0);
			expect(policies.join('\n'), `${table} must not allow using (true)`).not.toMatch(
				/using\s*\(\s*true\s*\)/i
			);
		}
	});

	it('revokes direct execution of discussion trigger functions from every client role', () => {
		const discussionSql = readFileSync(DISCUSSION_MIGRATION, 'utf8');
		for (const functionName of ['apply_potd_vote_delta', 'validate_potd_comment']) {
			for (const role of ['public', 'anon', 'authenticated']) {
				expect(discussionSql, `${functionName} must revoke EXECUTE from ${role}`).toMatch(
					new RegExp(
						`revoke execute on function public\\.${functionName}\\([^)]*\\) from [^;]*\\b${role}\\b`,
						'i'
					)
				);
			}
		}
	});

	it('sets an empty search path on every discussion SECURITY DEFINER function', () => {
		const discussionSql = readFileSync(DISCUSSION_MIGRATION, 'utf8');
		const functions = [...discussionSql.matchAll(/create function public\.[\s\S]*?\$\$;/gi)].map(
			(match) => match[0]
		);
		const definers = functions.filter((definition) => /security definer/i.test(definition));
		expect(definers.length).toBeGreaterThan(0);
		for (const definition of definers) {
			expect(definition).toMatch(/set search_path\s*=\s*''/i);
		}
	});

	it('limits discussion comment writes to the granted columns', () => {
		const discussionSql = readFileSync(DISCUSSION_MIGRATION, 'utf8');
		expect(discussionSql).toMatch(
			/grant insert\s*\(\s*question_id\s*,\s*content\s*\)\s*on public\.potd_discussion_comments to authenticated/i
		);
		expect(discussionSql).toMatch(
			/grant update\s*\(\s*content\s*\)\s*on public\.potd_discussion_comments to authenticated/i
		);
		for (const table of ['potd_discussion_comments', 'potd_comment_votes']) {
			expect(discussionSql).not.toMatch(
				new RegExp(
					`grant\\s+(?:all(?:\\s+privileges)?|update)\\s+(?:on\\s+public\\.${table}|public\\.${table})\\s+to authenticated`,
					'i'
				)
			);
		}
		expect(discussionSql).toMatch(
			/grant insert\s*\(\s*comment_id\s*,\s*vote_value\s*\)\s*on public\.potd_comment_votes to authenticated/i
		);
		expect(discussionSql).toMatch(
			/grant update\s*\(\s*vote_value\s*\)\s*on public\.potd_comment_votes to authenticated/i
		);
	});

	it('requires a recorded POTD solve and unlocks discussion the day after its schedule date', () => {
		const discussionRules = readFileSync(DISCUSSION_RULES_MIGRATION, 'utf8');
		expect(discussionRules).toMatch(/and sq\.is_potd/);
		expect(discussionRules).toMatch(/\(now\(\) at time zone 'UTC'\)::date > s\.potd_date/);
	});

	it('caps all code snippets in a comment to six non-empty lines total', () => {
		const discussionRules = readFileSync(DISCUSSION_RULES_MIGRATION, 'utf8');
		expect(discussionRules).toMatch(/code_lines := code_lines \+/);
		expect(discussionRules).toMatch(/body_without_fenced_blocks/);
		expect(discussionRules).toMatch(/if code_lines > max_block then/);
	});

	it('guards POTD rating writes against invalid timing, attempts, and rating calculations', () => {
		const ratingGuard = readFileSync(
			join(MIGRATIONS_DIR, '20260928170000_guard_potd_rating_events.sql'),
			'utf8'
		);
		expect(ratingGuard).toMatch(/pg_advisory_xact_lock/);
		expect(ratingGuard).toMatch(/potd_solve_rating_only_available_on_scheduled_day/);
		expect(ratingGuard).toMatch(/potd_failure_requires_unsolved_attempt_on_scheduled_day/);
		expect(ratingGuard).toMatch(/potd_rating_calculation_mismatch/);
		expect(ratingGuard).toMatch(/before insert on public\.rating_event/);
		expect(ratingGuard).toMatch(/POTD rating tables are required before installing/);
	});
});
