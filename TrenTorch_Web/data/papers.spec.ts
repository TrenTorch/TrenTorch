import { describe, it, expect } from 'vitest';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { readPaperTopics } from '$processes/papers/read-papers';

// The /papers pages are built from the folders under data/app_data/12-research-papers
// (see the README there). These checks keep those folders consistent with the curriculum
// the exercises are served from.
const RESEARCH_ROOT = 'research-papers';

const topics = readPaperTopics();
const papers = topics.flatMap((topic) => topic.papers);
const linked = papers.flatMap((paper) => paper.implementations.map((impl) => ({ paper, impl })));

describe('research papers data', () => {
	it('has paper slugs that are unique', () => {
		const slugs = papers.map((paper) => paper.slug);
		expect(slugs.filter((slug, i) => slugs.indexOf(slug) !== i)).toEqual([]);
	});

	it('gives every paper exactly 3 implementations', () => {
		const wrong = papers
			.filter((paper) => paper.implementations.length !== 3)
			.map((paper) => `${paper.slug} (${paper.implementations.length})`);
		expect(wrong).toEqual([]);
	});

	it('links every implementation to a real question with the same difficulty', () => {
		const problems = linked.flatMap(({ paper, impl }) => {
			const question = questionsById.get(impl.slug);
			if (!question) return [`${paper.slug}: no question named ${impl.slug}`];
			if (question.root !== RESEARCH_ROOT) {
				return [`${paper.slug}: ${impl.slug} is not in the research-papers root`];
			}
			if (question.difficulty !== impl.difficulty) {
				return [
					`${paper.slug}: ${impl.slug} is ${question.difficulty} but listed as ${impl.difficulty}`
				];
			}
			return [];
		});
		expect(problems).toEqual([]);
	});

	it('links every research-papers question from exactly one paper', () => {
		const counts = new Map<string, number>();
		for (const { impl } of linked) counts.set(impl.slug, (counts.get(impl.slug) ?? 0) + 1);
		const questions = [...questionsById.values()].filter((q) => q.root === RESEARCH_ROOT);

		const unlinked = questions.filter((q) => !counts.has(q.id)).map((q) => q.id);
		const repeated = [...counts].filter(([, n]) => n > 1).map(([slug]) => slug);
		expect({ unlinked, repeated }).toEqual({ unlinked: [], repeated: [] });
		expect(questions.length).toBe(linked.length);
	});

	it('uses folder names without "and" or "vs" in them', () => {
		// Folder names become ids and URLs (/papers?track=<slug>), so they stay short; the readable
		// title (with "&") lives in meta.json.
		const slugs = [...topics.map((t) => t.slug), ...papers.map((p) => p.slug)];
		expect(slugs.filter((slug) => /(^|-)(and|vs)(-|$)/.test(slug))).toEqual([]);
	});
});
