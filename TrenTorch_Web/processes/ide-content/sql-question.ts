// SQL questions are authored like the others (README.md, starter.py, solution.py,
// tests.py) but their starter.py has two parts, split by markers:
//
//   -- @schema
//   CREATE TABLE ...;  INSERT ...;       <- loaded into a fresh SQLite database
//   -- @query
//   -- TODO: what to write               <- what the student sees in the editor
//
// The student's editor shows the CREATE statements as comments (so the columns
// are visible) followed by the query part. The schema itself is never part of
// the student's text, so it cannot be edited away or broken.
export const SCHEMA_MARKER = '-- @schema';
export const QUERY_MARKER = '-- @query';

export function isSqlQuestion(tags: readonly string[], id: string): boolean {
	return tags.includes('db') || id.startsWith('db-sql-');
}

export function splitSqlStarter(raw: string): { schema: string; query: string } {
	const text = raw.replace(/\r\n/g, '\n');
	const queryAt = text.indexOf(QUERY_MARKER);
	const schemaAt = text.indexOf(SCHEMA_MARKER);
	if (schemaAt === -1 || queryAt === -1 || queryAt < schemaAt) {
		return { schema: '', query: text.trim() };
	}
	return {
		schema: text.slice(schemaAt + SCHEMA_MARKER.length, queryAt).trim(),
		query: text.slice(queryAt + QUERY_MARKER.length).trim()
	};
}

// Statements of a schema block that define structure (not the sample rows).
function structureStatements(schema: string): string[] {
	return schema
		.split(/;[ \t]*(?:\n|$)/)
		.map((statement) => statement.trim())
		.filter((statement) => /^CREATE\s/i.test(statement));
}

export function buildSqlEditorStarter(raw: string): string {
	const { schema, query } = splitSqlStarter(raw);
	const structure = structureStatements(schema);
	const header = structure.length
		? [
				'-- Tables available (already created and filled for you):',
				'--',
				...structure.flatMap((statement) => [
					...statement.split('\n').map((line) => `--   ${line.trimEnd()}`.trimEnd()),
					'--'
				]),
				'-- Run (Ctrl/Cmd+Enter) executes your query; Submit checks it against the tests.',
				''
			].join('\n')
		: '';
	return `${header}\n${query}\n`.replace(/^\n+/, '');
}
