import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { PLOTLY_JS } from './load-plotly';

// platform/static/vendor holds third-party files served as they are. Their checksums are recorded in
// vendor.json, so a changed or corrupted file is noticed in review instead of at runtime.
const dir = join(import.meta.dirname, '..', '..', 'platform', 'static', 'vendor');
const manifest: { file: string; sha256: string; bytes: number }[] = JSON.parse(
	readFileSync(join(dir, 'vendor.json'), 'utf8')
);

describe('vendored files', () => {
	it.each(manifest.map((entry) => [entry.file, entry] as const))(
		'%s matches its recorded checksum and size',
		(_file, entry) => {
			const bytes = readFileSync(join(dir, entry.file));
			expect(bytes.length).toBe(entry.bytes);
			expect(createHash('sha256').update(bytes).digest('hex')).toBe(entry.sha256);
		}
	);

	it('includes the plotly.js file the chart viewer loads', () => {
		expect(manifest.map((entry) => entry.file)).toContain(PLOTLY_JS);
	});
});
