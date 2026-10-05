import { describe, expect, it } from 'vitest';
import { importedModules, MICROPIP_PACKAGES } from './ensure-packages';

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

	it('reads several sources and ignores text that only looks like an import', () => {
		const modules = importedModules('import pandas', '# import torch\nprint("import scipy")');
		expect([...modules]).toEqual(['pandas']);
	});

	it('pins every micropip package to an exact version', () => {
		for (const spec of Object.values(MICROPIP_PACKAGES)) expect(spec).toMatch(/==\d+\.\d+\.\d+$/);
	});
});
