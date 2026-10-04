import { describe, expect, it } from 'vitest';
import { buildSqlEditorStarter, isSqlQuestion, splitSqlStarter } from './sql-question';

const RAW = `-- @schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
INSERT INTO users VALUES (1, 'Alice');
CREATE INDEX idx_users_name ON users(name);
-- @query
-- TODO: Return every user.
`;

describe('isSqlQuestion', () => {
	it('recognises the db tag and the db-sql- id prefix', () => {
		expect(isSqlQuestion(['db'], 'anything')).toBe(true);
		expect(isSqlQuestion([], 'db-sql-select-all')).toBe(true);
		expect(isSqlQuestion(['numpy'], 'linear-forward')).toBe(false);
	});
});

describe('splitSqlStarter', () => {
	it('separates the schema from the query part', () => {
		const { schema, query } = splitSqlStarter(RAW);
		expect(schema).toContain('CREATE TABLE users');
		expect(schema).toContain("INSERT INTO users VALUES (1, 'Alice');");
		expect(schema).not.toContain('@query');
		expect(query).toBe('-- TODO: Return every user.');
	});

	it('treats a starter without markers as query only', () => {
		expect(splitSqlStarter('SELECT 1;')).toEqual({ schema: '', query: 'SELECT 1;' });
	});
});

describe('buildSqlEditorStarter', () => {
	const starter = buildSqlEditorStarter(RAW);

	it('shows the table definitions as comments but never the sample rows', () => {
		expect(starter).toContain('--   CREATE TABLE users (');
		expect(starter).toContain('--   CREATE INDEX idx_users_name ON users(name)');
		expect(starter).not.toContain('INSERT');
	});

	it('ends with the query part, and every schema line is a comment', () => {
		expect(starter.trimEnd().endsWith('-- TODO: Return every user.')).toBe(true);
		const beforeTask = starter.split('-- TODO')[0];
		for (const line of beforeTask.split('\n').filter(Boolean))
			expect(line.startsWith('--')).toBe(true);
	});
});
