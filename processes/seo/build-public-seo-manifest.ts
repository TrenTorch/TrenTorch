import { competitors } from '$data/competitors';
import { curriculum } from '$data/questions';
import { seoLandingPages } from '$data/seo-landing-pages';
import { questionsById } from '$processes/ide-content/curriculum-index';
import { absoluteUrl } from './absolute-url';
import { buildComparisonIndexSeo } from './build-comparison-index-seo';
import { buildComparisonSeo } from './build-comparison-seo';
import { buildFaqPageSeo } from './build-faq-page-seo';
import { buildHomeSeo } from './build-home-seo';
import { buildLandingPageSeo } from './build-landing-page-seo';
import { buildPotdSeo } from './build-potd-seo';
import { buildPartSeo } from './build-part-seo';
import { buildQuestionSeo } from './build-question-seo';
import { buildQuestionsIndexSeo } from './build-questions-index-seo';
import { latestLiveDate } from './latest-live-date';

export interface SeoRouteManifestEntry {
	path: string;
	type: 'home' | 'question' | 'track' | 'comparison' | 'landing' | 'faq' | 'static';
	indexable: boolean;
	prerendered: boolean;
	canonical: string;
	title: string;
	description: string;
	primaryIntent: string;
	source: string;
}

function createEntry(
	entry: Omit<SeoRouteManifestEntry, 'canonical' | 'prerendered'> & {
		prerendered?: boolean;
	}
): SeoRouteManifestEntry {
	return {
		...entry,
		prerendered: entry.prerendered ?? true,
		canonical: absoluteUrl(entry.path)
	};
}

export function buildPublicSeoManifest(today: string = latestLiveDate()): SeoRouteManifestEntry[] {
	const home = buildHomeSeo();
	const questions = buildQuestionsIndexSeo();
	const potd = buildPotdSeo();
	const faq = buildFaqPageSeo();
	const comparisonsIndex = buildComparisonIndexSeo();
	const staticEntries = [
		createEntry({
			path: home.path,
			type: 'home',
			indexable: true,
			title: home.title,
			description: home.description,
			primaryIntent: 'free machine-learning coding practice',
			source: 'platform/routes/+page.svelte'
		}),
		createEntry({
			path: questions.path,
			type: 'static',
			indexable: true,
			title: questions.title,
			description: questions.description,
			primaryIntent: 'machine-learning practice questions',
			source: 'platform/routes/questions/+page.svelte'
		}),
		createEntry({
			path: potd.path,
			type: 'static',
			indexable: true,
			title: potd.title,
			description: potd.description,
			primaryIntent: 'machine-learning Problem of the Day',
			source: 'platform/routes/potd/+page.svelte'
		}),
		createEntry({
			path: faq.path,
			type: 'faq',
			indexable: true,
			title: faq.title,
			description: faq.description,
			primaryIntent: 'TrenTorch frequently asked questions',
			source: 'platform/routes/faq/+page.svelte'
		}),
		createEntry({
			path: comparisonsIndex.path,
			type: 'comparison',
			indexable: true,
			title: comparisonsIndex.title,
			description: comparisonsIndex.description,
			primaryIntent: 'machine-learning practice alternatives',
			source: 'platform/routes/compare/+page.svelte'
		}),
		...[
			{
				path: '/contact',
				title: 'Contact | TrenTorch',
				description: 'Get in touch with the TrenTorch team.',
				intent: 'contact TrenTorch'
			},
			{
				path: '/privacy',
				title: 'Privacy | TrenTorch',
				description: 'Privacy policy for TrenTorch.',
				intent: 'TrenTorch privacy policy'
			},
			{
				path: '/terms',
				title: 'Terms | TrenTorch',
				description: 'Terms of use for TrenTorch.',
				intent: 'TrenTorch terms of use'
			}
		].map((page) =>
			createEntry({
				path: page.path,
				type: 'static',
				indexable: true,
				title: page.title,
				description: page.description,
				primaryIntent: page.intent,
				source: `platform/routes/${page.path.slice(1)}/+page.svelte`
			})
		)
	];

	const trackEntries = curriculum.map((part) => {
		const seo = buildPartSeo(part);
		return createEntry({
			path: seo.path,
			type: 'track',
			indexable: true,
			title: seo.title,
			description: seo.description,
			primaryIntent: `${part.title} practice questions`,
			source: 'platform/routes/questions/[partId]/+page.svelte'
		});
	});

	const questionIds = new Set(questionsById.keys());
	for (const part of curriculum)
		for (const track of part.tracks)
			for (const question of track.questions) questionIds.add(question.slug);

	const questionEntries = [...questionIds].map((id) => {
		const seo = buildQuestionSeo(id, today);
		return createEntry({
			path: seo.path,
			type: 'question',
			indexable: seo.indexable,
			title: seo.title,
			description: seo.description,
			primaryIntent: `practice problem: ${seo.title}`,
			source: 'platform/routes/ide/[id]/+page.server.ts'
		});
	});

	const landingEntries = seoLandingPages.map((page) => {
		const seo = buildLandingPageSeo(page);
		return createEntry({
			path: seo.path,
			type: 'landing',
			indexable: true,
			title: seo.title,
			description: seo.description,
			primaryIntent: page.primaryIntent,
			source: 'data/seo-landing-pages.ts'
		});
	});

	const comparisonEntries = competitors.map((competitor) => {
		const seo = buildComparisonSeo(competitor);
		return createEntry({
			path: seo.path,
			type: 'comparison',
			indexable: true,
			title: seo.title,
			description: seo.description,
			primaryIntent: `${competitor.name} alternative for machine learning`,
			source: 'data/competitors.ts'
		});
	});

	return [
		...staticEntries,
		...trackEntries,
		...questionEntries,
		...landingEntries,
		...comparisonEntries
	];
}
