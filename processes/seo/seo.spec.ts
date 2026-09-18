import { describe, it, expect } from 'vitest';
import { potdEntries } from '$data/potd';
import { buildFaqEntries, FAQ_DISCLAIMER } from '$data/faq';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { absoluteUrl } from './absolute-url';
import { buildFaqJsonLd } from './build-faq-json-ld';
import { buildQuestionSeo } from './build-question-seo';
import { buildSitemapXml } from './build-sitemap-xml';
import { latestLiveDate } from './latest-live-date';
import { listSitemapPaths } from './list-sitemap-paths';
import { toJsonLdScript } from './to-json-ld-script';
import { truncate } from './truncate';

describe('absoluteUrl', () => {
	it('keeps a trailing slash only on the homepage', () => {
		expect(absoluteUrl('/')).toBe('https://trentorch.com/');
		expect(absoluteUrl('/questions/')).toBe('https://trentorch.com/questions');
		expect(absoluteUrl('ide/x')).toBe('https://trentorch.com/ide/x');
	});
});

describe('toJsonLdScript', () => {
	it('cannot be closed early by text inside the data', () => {
		const script = toJsonLdScript({ name: '</script><script>alert(1)</script>' });
		const inner = script.slice(script.indexOf('>') + 1, script.lastIndexOf('</script>'));
		expect(inner).not.toContain('<');
		expect(JSON.parse(inner).name).toBe('</script><script>alert(1)</script>');
	});
});

describe('latestLiveDate', () => {
	it('is the date already reached in the earliest timezone (UTC+14)', () => {
		expect(latestLiveDate(new Date('2026-09-18T20:00:00Z'))).toBe('2026-09-19');
		expect(latestLiveDate(new Date('2026-09-18T09:59:00Z'))).toBe('2026-09-18');
	});
});

describe('truncate', () => {
	it('leaves short text alone and cuts long text at a word boundary', () => {
		expect(truncate('short text', 160)).toBe('short text');
		const out = truncate('word '.repeat(60), 50);
		expect(out.length).toBeLessThanOrEqual(50);
		expect(out.endsWith('…')).toBe(true);
		expect(out).not.toMatch(/wor…$/);
	});
});

describe('buildQuestionSeo', () => {
	const [slug, question] = [...questionsById.entries()][0];

	it('gives an authored question its own title, a bounded description, and structured data', () => {
		const seo = buildQuestionSeo(slug, '2099-01-01');
		expect(seo.indexable).toBe(true);
		expect(seo.title).toBe(`${question.title} | TrenTorch`);
		expect(seo.description.length).toBeLessThanOrEqual(160);
		expect(seo.path).toBe(`/ide/${slug}`);
		const types = seo.jsonLd.map((block) => (block as { '@type': string })['@type']);
		expect(types).toEqual(['LearningResource', 'BreadcrumbList']);
		expect(seo.jsonLd[0]).toMatchObject({ isAccessibleForFree: true });
	});

	it('marks a slug without authored content as not indexable', () => {
		const seo = buildQuestionSeo('this-question-does-not-exist', '2099-01-01');
		expect(seo.indexable).toBe(false);
		expect(seo.jsonLd).toEqual([]);
	});

	it('keeps a future-dated Problem of the Day out of search until its date', () => {
		const entry = potdEntries[potdEntries.length - 1];
		expect(buildQuestionSeo(entry.questionId, '2000-01-01').indexable).toBe(false);
		expect(buildQuestionSeo(entry.questionId, entry.date).indexable).toBe(true);
	});
});

describe('listSitemapPaths', () => {
	const paths = listSitemapPaths('2099-01-01');

	it('lists the static pages, every section page, and authored questions', () => {
		expect(paths).toEqual(expect.arrayContaining(['/', '/questions', '/potd', '/faq']));
		expect(paths.some((p) => p.startsWith('/questions/part-'))).toBe(true);
		expect(paths.some((p) => p.startsWith('/ide/'))).toBe(true);
	});

	it('has no duplicates and leaves out the user-specific account page', () => {
		expect(new Set(paths).size).toBe(paths.length);
		expect(paths).not.toContain('/account');
	});

	it('only lists /ide/ pages that have authored content', () => {
		const ide = paths.filter((p) => p.startsWith('/ide/')).map((p) => p.slice('/ide/'.length));
		expect(ide.length).toBeGreaterThan(0);
		for (const id of ide) expect(questionsById.has(id)).toBe(true);
	});

	it('does not advertise a Problem of the Day before its date', () => {
		const entry = potdEntries[potdEntries.length - 1];
		expect(listSitemapPaths('2000-01-01')).not.toContain(`/ide/${entry.questionId}`);
		expect(listSitemapPaths(entry.date)).toContain(`/ide/${entry.questionId}`);
	});
});

describe('buildSitemapXml', () => {
	it('emits one absolute <loc> per path', () => {
		const xml = buildSitemapXml('2099-01-01');
		expect(xml.startsWith('<?xml version="1.0" encoding="UTF-8"?>')).toBe(true);
		expect(xml).toContain('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">');
		expect(xml.match(/<loc>/g)?.length).toBe(listSitemapPaths('2099-01-01').length);
		expect(xml).toContain('<loc>https://trentorch.com/faq</loc>');
	});
});

describe('FAQ copy', () => {
	const entries = buildFaqEntries(356);
	const allText = entries.map((e) => `${e.question} ${e.answer}`).join(' ');

	it('states the real licence, not an open-source or MIT claim', () => {
		expect(allText).toContain('PolyForm Noncommercial');
		expect(allText).not.toMatch(/\bMIT\b/);
		expect(allText).not.toMatch(/open[- ]source/i);
	});

	it('does not claim a CUDA judge the site cannot run', () => {
		expect(allText).toContain('you do not write or compile CUDA');
	});

	it('names each platform it mentions in the trademark disclaimer', () => {
		for (const name of ['TensorTonic', 'DeepML', 'LeetCode']) {
			if (allText.includes(name)) expect(FAQ_DISCLAIMER).toContain(name);
		}
	});

	it('states no price or feature claim about another platform', () => {
		expect(allText).not.toMatch(/\$\d|per month|subscription/i);
	});

	it('is mirrored exactly by the FAQPage structured data', () => {
		const schema = buildFaqJsonLd(entries);
		expect(schema['@type']).toBe('FAQPage');
		expect(schema.mainEntity).toHaveLength(entries.length);
		schema.mainEntity.forEach((item, i) => {
			expect(item.name).toBe(entries[i].question);
			expect(item.acceptedAnswer.text).toBe(entries[i].answer);
		});
	});
});
