import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { potdEntries } from '../data/potd';
import { scheduleRows } from '../processes/potd/potd-schedule-sql.mjs';

// record_potd_attempt() / record_potd_outcome() reject any question missing
// from public.potd_schedule, so a POTD added to data/potd.ts without a
// matching schedule row silently breaks saving and rating for that whole day.
// If this fails, run `npm run potd:schedule-sql` and commit the output as a
// new migration (then apply it to Supabase).
const MIGRATIONS_DIR = join(import.meta.dirname, 'migrations');
const sql = readdirSync(MIGRATIONS_DIR)
	.filter((name) => name.endsWith('.sql'))
	.sort()
	.map((name) => readFileSync(join(MIGRATIONS_DIR, name), 'utf8'))
	.join('\n');

describe('potd_schedule migrations', () => {
	const rows = scheduleRows(potdEntries);

	it.each(rows.map((r) => [r.date, r.questionId, r.difficulty]))(
		'schedules the POTD for %s (%s) as %s',
		(date, questionId, difficulty) => {
			expect(sql).toContain(`('${questionId}', '${date}', '${difficulty}')`);
		}
	);
});
