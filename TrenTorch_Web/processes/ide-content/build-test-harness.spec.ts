import { describe, it, expect } from 'vitest';
import { questionsById } from './curriculum-index';
import { buildTestHarness } from './build-test-harness';

describe('buildTestHarness', () => {
	it('resolves a cross-track load_solution dependency (regression: adaboost depending on decision-trees)', () => {
		// ensembles-adaboost (01-classical-ml/04-ensembles) depends on
		// 03-decision-trees/03-best-split-minimal-tree's build_tree/
		// predict_tree -- a DIFFERENT track under the same section. This
		// used to crash with `RuntimeError: Missing track-mate dependency
		// '03-best-split-minimal-tree'` because dependency resolution was
		// scoped to the current question's own track and keyed by bare
		// folder name, even though the folder name alone is only unique
		// within one track (see curriculum-index.ts's questionsByFullPath
		// comment).
		const question = questionsById.get('ensembles-adaboost');
		expect(question).toBeDefined();

		const harness = buildTestHarness(question!);

		expect(harness).not.toContain('Missing dependency');
		expect(harness).not.toContain('Missing track-mate dependency');
		expect(harness).toContain('def build_tree');
		expect(harness).toContain('def predict_tree');
	});

	it('still resolves same-track dependencies correctly', () => {
		// 02-classification/05-training-loop depends on both a same-track
		// dependency (01-sigmoid, 03-bce-gradient) and cross-track ones
		// (01-linear-regression/01-hypothesis-function, 04-gd-step) --
		// exercises both paths through the same lookup.
		const question = questionsById.get('classification-training-loop');
		expect(question).toBeDefined();

		const harness = buildTestHarness(question!);

		expect(harness).not.toContain('Missing dependency');
		expect(harness).toContain('def sigmoid');
		expect(harness).toContain('def linear');
	});

	it('keeps a module-level test fixture that sits between the load_solution aliases and the first def (regression: _X undefined in the browser IDE)', () => {
		// 05-data-preprocessing/01-detecting-missing-values defines a shared
		// `_X` fixture array (and `nan = np.nan`) right after its
		// load_solution aliases, before its first `def test_...`. An
		// earlier version of stripLoadSolutionBoilerplate treated
		// "import line through first top-level def" as one solid block of
		// boilerplate to delete, silently deleting this fixture along with
		// it -- every test referencing `_X` then failed in the browser IDE
		// with `NameError: name '_X' is not defined`, even for a correct,
		// unmodified copy of the oracle solution (standalone `pytest
		// tests.py` never caught this, since none of this stripping runs
		// there).
		const question = questionsById.get('math-detecting-missing-values');
		expect(question).toBeDefined();

		const harness = buildTestHarness(question!);

		expect(harness).toContain('_X = np.array(');
		expect(harness).toContain('nan = np.nan');
		expect(harness).not.toContain('from _load import load_solution');
	});

	it('keeps helper classes defined between the load_solution aliases and the first def (regression: same class of bug as _X, for class-shaped fixtures)', () => {
		// 03-dl-training/02-layers/06-sequential-container defines two
		// small helper classes (AddConstant, MultiplyConstant) between its
		// load_solution aliases and its first `def test_...` -- the exact
		// same "real content living in the boilerplate's old strip range"
		// shape as the _X case above, just a class instead of an array.
		const question = questionsById.get('dl-training-sequential-container');
		expect(question).toBeDefined();

		const harness = buildTestHarness(question!);

		expect(harness).toContain('class AddConstant(Module):');
		expect(harness).toContain('class MultiplyConstant(Module):');
	});
});
