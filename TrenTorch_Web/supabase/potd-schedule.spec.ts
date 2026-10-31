import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { potdEntries } from '../data/potd';

// record_potd_attempt() / record_potd_outcome() reject any question missing
// from public.potd_schedule, so a POTD added to data/potd.ts without a
// matching schedule row silently breaks saving and rating for that whole day.
const MIGRATIONS_DIR = join(import.meta.dirname, 'migrations');
const sql = readdirSync(MIGRATIONS_DIR)
	.filter((name) => name.endsWith('.sql'))
	.sort()
	.map((name) => readFileSync(join(MIGRATIONS_DIR, name), 'utf8'))
	.join('\n');

describe('potd_schedule migrations', () => {
	it.each(potdEntries.map((e) => [e.date, e.questionId]))(
		'schedules the POTD for %s (%s)',
		(date, questionId) => {
			expect(sql).toContain(`('${questionId}', '${date}', `);
		}
	);
});
