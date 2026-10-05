import { describe, expect, it } from 'vitest';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { BUNDLED_WHEELS, importedModules } from './ensure-packages';

describe('importedModules', () => {
	it('finds top-level modules from import and from-import lines', () => {
		const code = `import numpy as np\nimport pandas as pd, os\nfrom matplotlib import pyplot as plt\n  import seaborn.objects as so\nfrom plotly.express import scatter`;
		expect([...importedModules(code)].sort()).toEqual([
			'matplotlib',
			'numpy',
			'pandas',
			'plotly',
			'seaborn'
		]);
	});

	it('does not try to load pytest, which the runner provides itself', () => {
		expect([...importedModules('import pytest\nimport pandas as pd')]).toEqual(['pandas']);
	});

	it('reads several sources and ignores text that only looks like an import', () => {
		const modules = importedModules('import pandas', '# import torch\nprint("import scipy")');
		expect([...modules]).toEqual(['pandas']);
	});
});

describe('bundled wheels', () => {
	const dir = join(import.meta.dirname, '..', '..', 'platform', 'static', 'wheels');
	const manifest: { file: string; sha256: string; bytes: number; url: string }[] = JSON.parse(
		readFileSync(join(dir, 'wheels.json'), 'utf8')
	);

	it('lists every wheel the loader installs, and nothing else', () => {
		const used = Object.values(BUNDLED_WHEELS).flatMap((entry) => entry.wheels);
		expect(manifest.map((entry) => entry.file).sort()).toEqual([...used].sort());
	});

	it.each(manifest.map((entry) => [entry.file, entry] as const))(
		'%s on disk matches its recorded checksum and size',
		(_file, entry) => {
			const bytes = readFileSync(join(dir, entry.file));
			expect(bytes.length).toBe(entry.bytes);
			expect(createHash('sha256').update(bytes).digest('hex')).toBe(entry.sha256);
		}
	);

	it('are pure-Python wheels pinned to an exact version', () => {
		for (const entry of manifest)
			expect(entry.file).toMatch(/^[a-z_]+-\d+\.\d+\.\d+-py3-none-any\.whl$/);
	});

	it('only needs packages that Pyodide ships', () => {
		const pyodide = new Set(['numpy', 'pandas', 'matplotlib', 'packaging']);
		for (const entry of Object.values(BUNDLED_WHEELS)) {
			for (const name of entry.requires) expect(pyodide.has(name)).toBe(true);
		}
	});
});
