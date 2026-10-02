import type { Competitor } from '$data/competitors';
import { buildBreadcrumbJsonLd } from './build-breadcrumb-json-ld';
import { buildFaqJsonLd } from './build-faq-json-ld';
import { buildSiteJsonLd } from './build-site-json-ld';
import { absoluteUrl } from './absolute-url';
import { CLAIMS, getLiveClaimText } from './claims';
import { truncate } from './truncate';
import { withSiteName } from './with-site-name';

export function buildComparisonFaqs(competitor: Competitor) {
	return [
		{
			question: `Is TrenTorch an alternative to ${competitor.name} for machine-learning practice?`,
			answer: `TrenTorch is ${getLiveClaimText(['freePractice'])[0]}. Learners can ${getLiveClaimText(['fromScratch', 'hiddenTestGrading']).join(' and ')}. ${competitor.summary} Review the linked official sources and curriculum to decide which product fits your needs.`
		},
		{
			question: `What does ${competitor.name} offer?`,
			answer: `${competitor.summary} The facts on this page were checked against the official pages linked below on ${competitor.verifiedOn}.`
		}
	];
}

export function buildComparisonSeo(competitor: Competitor) {
	const path = `/compare/${competitor.slug}`;
	const description = truncate(
		`Looking for a ${competitor.name} alternative for machine-learning practice? TrenTorch offers ${CLAIMS.freePractice.text} and hands-on coding problems.`,
		160
	);
	const faqs = buildComparisonFaqs(competitor);

	return {
		title: withSiteName(`${competitor.name} alternative for machine learning`),
		description,
		path,
		jsonLd: [
			buildSiteJsonLd(),
			{
				'@context': 'https://schema.org',
				'@type': 'CollectionPage',
				name: `${competitor.name} alternative for machine learning`,
				description,
				url: absoluteUrl(path),
				inLanguage: 'en',
				isAccessibleForFree: true
			},
			buildFaqJsonLd(faqs),
			buildBreadcrumbJsonLd([
				{ name: 'Home', path: '/' },
				{ name: 'Alternatives', path: '/compare' },
				{ name: `${competitor.name} alternative`, path }
			])
		]
	};
}
