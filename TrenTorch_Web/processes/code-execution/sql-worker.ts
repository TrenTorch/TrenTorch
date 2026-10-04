import { initializePyodide } from './initialize-pyodide';
import { toBase64 } from './to-base64';

self.onmessage = async (e: MessageEvent) => {
	const trustedOrigins = new Set([self.location.origin, 'null']);
	const messageOrigin = typeof e.origin === 'string' ? e.origin : '';
	if (messageOrigin && !trustedOrigins.has(messageOrigin)) {
		self.postMessage({ type: 'error', error: `Untrusted message origin: ${messageOrigin}` });
		return;
	}

	const { id, action, query, dbSchema, testCode, contentId } = e.data;

	try {
		const py = await initializePyodide();

		if (action === 'init') {
			self.postMessage({ id, type: 'init_complete', success: true });
			return;
		}

		if (action === 'run') {
			self.postMessage({ type: 'status', status: 'running' });
			const startTime = performance.now();

			const pythonScript = `
import sqlite3
import json
import sys
from io import StringIO

# Create in-memory database
db = sqlite3.connect(':memory:')
db.row_factory = sqlite3.Row
cursor = db.cursor()

# Setup schema if provided
schema = """${dbSchema || ''}"""
if schema.strip():
    for statement in schema.split(';'):
        if statement.strip():
            try:
                cursor.execute(statement.strip())
            except Exception as e:
                pass

# Execute user query
query = """${query}"""
stdout_capture = StringIO()
stderr_capture = StringIO()
error = None

try:
    cursor.execute(query)
    results = cursor.fetchall()

    if cursor.description:
        columns = [description[0] for description in cursor.description]
        rows = [dict(zip(columns, row)) for row in results]
        output = json.dumps({'columns': columns, 'rows': rows, 'count': len(rows)})
    else:
        output = f"Query executed. Rows affected: {cursor.rowcount}"
except Exception as e:
    import traceback
    error = traceback.format_exc()
    output = ""

db.close()

json.dumps({
    'output': output,
    'error': error
})
`;

			try {
				const result = await py.runPythonAsync(pythonScript);
				const parsed = JSON.parse(result);
				const durationMs = Math.round(performance.now() - startTime);

				// Format output as readable table if it's JSON
				let displayOutput = parsed.output;
				try {
					const data = JSON.parse(parsed.output);
					if (data.columns && data.rows) {
						displayOutput = `Results (${data.count} rows):\n`;
						displayOutput += data.columns.join(' | ') + '\n';
						displayOutput += '-'.repeat(data.columns.join(' | ').length) + '\n';
						data.rows.forEach((row: any) => {
							displayOutput +=
								data.columns.map((col: string) => String(row[col] || '')).join(' | ') +
								'\n';
						});
					}
				} catch {
					// If not JSON, use output as-is
				}

				self.postMessage({
					id,
					type: 'run_result',
					success: !parsed.error,
					output: displayOutput,
					error: parsed.error,
					durationMs
				});
			} catch (err: any) {
				const durationMs = Math.round(performance.now() - startTime);
				self.postMessage({
					id,
					type: 'run_result',
					success: false,
					output: '',
					error: err.message || String(err),
					durationMs
				});
			}

			self.postMessage({ type: 'status', status: 'ready' });
			return;
		}

		if (action === 'test') {
			self.postMessage({ type: 'status', status: 'running' });
			const startTime = performance.now();

			const pythonScript = `
import sqlite3
import json
import sys
from io import StringIO

# Create in-memory database with schema
db = sqlite3.connect(':memory:')
db.row_factory = sqlite3.Row
cursor = db.cursor()

schema = """${dbSchema}"""
for statement in schema.split(';'):
    if statement.strip():
        try:
            cursor.execute(statement.strip())
        except:
            pass

# Run tests
test_code = '''${testCode}'''
exec_globals = {'sqlite3': sqlite3, 'cursor': cursor, 'db': db}
results = []
passed = 0
failed = 0
error = None

try:
    # Expected: test_code defines test functions or assertions
    exec(test_code, exec_globals)
except Exception as e:
    import traceback
    error = traceback.format_exc()

db.close()

json.dumps({
    'passed': passed,
    'failed': failed,
    'error': error,
    'results': results
})
`;

			try {
				const result = await py.runPythonAsync(pythonScript);
				const parsed = JSON.parse(result);
				const durationMs = Math.round(performance.now() - startTime);

				self.postMessage({
					id,
					type: 'test_result',
					contentId,
					totalTests: parsed.passed + parsed.failed,
					passedTests: parsed.passed,
					failedTests: parsed.failed,
					allPassed: parsed.failed === 0 && !parsed.error,
					totalDurationMs: durationMs,
					results: parsed.results || [],
					rawOutput: parsed.results?.join('\n') || '',
					error: parsed.error,
					isSample: false
				});
			} catch (err: any) {
				const durationMs = Math.round(performance.now() - startTime);
				self.postMessage({
					id,
					type: 'test_result',
					contentId,
					totalTests: 0,
					passedTests: 0,
					failedTests: 0,
					allPassed: false,
					totalDurationMs: durationMs,
					results: [],
					rawOutput: '',
					error: err.message || String(err),
					isSample: false
				});
			}

			self.postMessage({ type: 'status', status: 'ready' });
			return;
		}
	} catch (err: any) {
		self.postMessage({
			id,
			type: 'error',
			error: err.message || String(err)
		});
	}
};
