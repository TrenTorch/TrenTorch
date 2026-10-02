import { describe, it, expect } from 'vitest';
import { potdEntries } from '$data/potd';
import { competitors } from '$data/competitors';
import { curriculum } from '$data/questions';
import { seoLandingPages } from '$data/seo-landing-pages';
import { buildFaqEntries, FAQ_DISCLAIMER } from '$data/faq';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { absoluteUrl } from './absolute-url';
import { buildComparisonSeo } from './build-comparison-seo';
import { buildHomeSeo } from './build-home-seo';
import { buildLandingPageSeo } from './build-landing-page-seo';
import { buildFaqJsonLd } from './build-faq-json-ld';
import { buildPublicSeoManifest } from './build-public-seo-manifest';
import { buildQuestionSeo } from './build-question-seo';
import { buildSitemapXml } from './build-sitemap-xml';
import { CLAIMS, getLiveClaimText } from './claims';
import { latestLiveDate } from './latest-live-date';
import { listSitemapPaths } from './list-sitemap-paths';
import { toJsonLdScript } from './to-json-ld-script';
import { truncate } from './truncate';
import { validatePublicSeoManifest } from './validate-public-seo-manifest';

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
		expect(paths).toEqual(expect.arrayContaining(['/', '/questions', '/potd', '/faq', '/compare']));
		expect(paths.some((p) => p.startsWith('/questions/part-'))).toBe(true);
		expect(paths.some((p) => p.startsWith('/ide/'))).toBe(true);
		for (const page of seoLandingPages) expect(paths).toContain(`/${page.slug}`);
		for (const competitor of competitors) expect(paths).toContain(`/compare/${competitor.slug}`);
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

describe('claims registry', () => {
	it('omits disabled claims from public copy', () => {
		expect(CLAIMS.researchPaperImplementations.live).toBe(false);
		expect(getLiveClaimText(['researchPaperImplementations'])).toEqual([]);
		expect(getLiveClaimText(['fromScratch'])).toEqual([CLAIMS.fromScratch.text]);
	});
});

describe('data-driven SEO routes', () => {
	it('maps every landing guide to existing curriculum sections and live claims', () => {
		const partIds = new Set(curriculum.map((part) => part.id));
		for (const page of seoLandingPages) {
			expect(page.partIds.length).toBeGreaterThan(0);
			for (const partId of page.partIds) expect(partIds.has(partId)).toBe(true);
			for (const claimKey of page.claimKeys) expect(CLAIMS[claimKey].live).toBe(true);
			const seo = buildLandingPageSeo(page);
			expect(seo.path).toBe(`/${page.slug}`);
			expect(seo.description).toBeTruthy();
		}
	});

	it('uses verified competitor entries and source links to generate comparison pages', () => {
		expect(competitors.map((competitor) => competitor.slug)).toEqual(['tensortonic', 'deep-ml']);
		for (const competitor of competitors) {
			expect(competitor.verifiedOn).toMatch(/^\d{4}-\d{2}-\d{2}$/);
			expect(competitor.sources.length).toBeGreaterThan(0);
			for (const source of competitor.sources) {
				expect(source.url).toMatch(
					new RegExp(`^${new URL(competitor.url).origin.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`)
				);
			}
			if (competitor.hasDailyProblemAndRating === 'partial') {
				expect(competitor.capabilityNotes.hasDailyProblemAndRating).toContain(
					'rating was not confirmed'
				);
			}
			const seo = buildComparisonSeo(competitor);
			expect(seo.path).toBe(`/compare/${competitor.slug}`);
			expect(seo.title).toContain(`${competitor.name} alternative`);
		}
	});

	it('validates metadata, canonicals, prerendering, and sitemap coverage across public routes', () => {
		const manifest = buildPublicSeoManifest('2099-01-01');
		const paths = listSitemapPaths('2099-01-01');
		expect(validatePublicSeoManifest(manifest, paths)).toEqual([]);
		expect(manifest.filter((entry) => entry.type === 'question' && entry.indexable)).toHaveLength(
			questionsById.size
		);
		expect(manifest.find((entry) => entry.path === '/')?.title).toBe(buildHomeSeo().title);
	});

	it('reports broken sitemap and indexability invariants', () => {
		const invalid = [
			{
				path: '/broken',
				type: 'landing' as const,
				indexable: true,
				prerendered: false,
				canonical: 'not a URL',
				title: '',
				description: '',
				primaryIntent: '',
				source: ''
			}
		];
		expect(validatePublicSeoManifest(invalid, [])).toEqual(
			expect.arrayContaining([
				'Missing title: /broken',
				'Missing description: /broken',
				'Missing primary intent: /broken',
				'Missing SEO copy source: /broken',
				'Indexable page is not prerendered: /broken',
				'Malformed canonical URL: /broken',
				'Indexable route missing from sitemap: /broken'
			])
		);
	});
});

describe('FAQ copy', () => {
	const entries = buildFaqEntries(356);
	const allText = entries.map((e) => `${e.question} ${e.answer}`).join(' ');

	it('accurately describes the noncommercial source license', () => {
		expect(allText).toContain('PolyForm Noncommercial');
		expect(allText).not.toMatch(/\bMIT\b/);
		expect(allText).toContain('source-available, not an OSI-approved open-source license');
	});

	it('does not claim a CUDA judge the site cannot run', () => {
		expect(allText).toContain('without compiling arbitrary CUDA C');
	});

	it('names each platform it mentions in the trademark disclaimer', () => {
		for (const name of ['TensorTonic', 'Deep-ML', 'LeetCode', 'Codeforces']) {
			if (allText.includes(name)) expect(FAQ_DISCLAIMER).toContain(name);
		}
	});

	it('does not make unverified negative claims about another platform', () => {
		expect(allText).not.toMatch(
			/(?:TensorTonic|Deep-ML)\s+(?:doesn't|does not|lacks|cannot|can't)/i
		);
		expect(allText).not.toMatch(/\$\d|per month/i);
		for (const competitor of competitors) {
			expect(competitor.sources.every((source) => source.url.startsWith(competitor.url))).toBe(
				true
			);
			expect(
				Object.values(competitor).filter((value) =>
					['yes', 'no', 'partial', 'unverified'].includes(String(value))
				)
			).not.toContain('no');
		}
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
