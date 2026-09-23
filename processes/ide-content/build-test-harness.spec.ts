import { describe, it, expect } from 'vitest';
import { questionsById } from './curriculum-index';
import { buildTestHarness } from './build-test-harness';
import { STUDENT_CODE_MARKER } from './harness-marker';

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

describe('buildTestHarness: what the student can use, and when', () => {
	function sections(id: string) {
		const question = questionsById.get(id);
		expect(question, `question ${id} exists`).toBeDefined();
		const harness = buildTestHarness(question!);
		const at = harness.indexOf(STUDENT_CODE_MARKER);
		expect(at, 'the harness has a marker between its two sections').toBeGreaterThan(-1);
		return { before: harness.slice(0, at), after: harness.slice(at) };
	}

	it('defines dependency classes before the student code, so a subclass of one can be defined (regression: NameError Module)', () => {
		// dl-training-lazylinear's starter subclasses a Module from an earlier
		// question. Defined after the student's code, `class LazyLinear(Module)`
		// crashed before any test ran.
		const { before, after } = sections('dl-training-lazylinear');

		expect(before).toContain('class Module');
		expect(after).not.toContain('class Module');
		expect(after).toContain('def test_');
	});

	it('binds a renamed import before the student code (regression: NameError softmax_axis1)', () => {
		// The starter has `softmax_axis1 = load_solution("...").softmax`. That line
		// is removed from student code, and only `softmax` is defined by the
		// dependency, so `softmax_axis1` used to be undefined.
		const { before } = sections('seq-attention-softmax-last-axis');

		expect(before).toContain('def softmax(');
		expect(before).toContain('softmax_axis1 = softmax');
	});

	it('resolves load_solution calls made inside a test body (regression: NameError load_solution)', () => {
		// math-mutual-information calls load_solution(".../01-entropy").entropy in a
		// test. That solution has to be defined, and load_solution has to exist.
		const { before, after } = sections('math-mutual-information');

		expect(before).toContain('def entropy(');
		expect(before).toContain('def load_solution(');
		expect(after).toContain(
			'load_solution("02-math-and-statistics/04-information-theory/01-entropy")'
		);
	});

	it('gives a module variable the tests use as a namespace a value (regression: NameError plain_gb)', () => {
		const { before, after } = sections('ensembles-regularized-boosting');

		expect(before).toContain('def train_gradient_boosting');
		expect(after).toContain(
			'plain_gb = load_solution("03-classical-ml/04-ensembles/04-full-boosting-loop")'
		);
	});

	it('does not turn a one-function alias into a module object', () => {
		// `find_best_split = load_solution(...).find_best_split` is the function
		// itself, already defined by the dependency, and must stay a function.
		const { after } = sections('ensembles-histogram-boosting');

		expect(after).not.toContain('find_best_split = _Namespace');
	});

	it('adds nothing for a question that needs neither', () => {
		const { before } = sections('math-detecting-missing-values');

		expect(before).not.toContain('def load_solution(');
		expect(before).not.toContain('_Namespace');
	});
});
