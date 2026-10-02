import { curriculum } from '$data/questions';
import type { SeoLandingPage } from '$data/seo-landing-pages';
import { buildSiteJsonLd } from './build-site-json-ld';
import { absoluteUrl } from './absolute-url';
import { buildBreadcrumbJsonLd } from './build-breadcrumb-json-ld';
import { buildFaqJsonLd } from './build-faq-json-ld';
import { CLAIMS, getLiveClaimText } from './claims';
import { truncate } from './truncate';
import { withSiteName } from './with-site-name';

export function buildLandingPageFaqs(page: SeoLandingPage) {
	return page.faqs.map((faq) => ({
		question: faq.question,
		answer: [faq.answerLead, ...getLiveClaimText(faq.claimKeys)].join(' ')
	}));
}

export function buildLandingPageSeo(page: SeoLandingPage) {
	const path = `/${page.slug}`;
	const parts = curriculum.filter((part) => page.partIds.includes(part.id));
	const questionCount = parts.reduce(
		(count, part) =>
			count + part.tracks.reduce((trackCount, track) => trackCount + track.questions.length, 0),
		0
	);
	const description = truncate(
		`TrenTorch offers ${CLAIMS.freePractice.text}. Explore ${page.primaryIntent} through ${questionCount} curriculum problems across ${parts.length} sections.`,
		160
	);
	const faqs = buildLandingPageFaqs(page);

	return {
		title: withSiteName(page.title),
		description,
		path,
		jsonLd: [
			buildSiteJsonLd(),
			{
				'@context': 'https://schema.org',
				'@type': 'CollectionPage',
				name: page.title,
				description,
				url: absoluteUrl(path),
				inLanguage: 'en',
				isAccessibleForFree: true
			},
			buildFaqJsonLd(faqs),
			buildBreadcrumbJsonLd([
				{ name: 'Home', path: '/' },
				{ name: page.title, path }
			])
		]
	};
}
