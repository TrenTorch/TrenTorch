import type { Part } from '$data/questions';
import { absoluteUrl } from './absolute-url';
import { buildBreadcrumbJsonLd } from './build-breadcrumb-json-ld';
import { truncate } from './truncate';
import { withSiteName } from './with-site-name';

export function buildPartSeo(part: Part) {
	const path = `/questions/${part.id}`;
	const questionCount = part.tracks.reduce((sum, track) => sum + track.questions.length, 0);
	const trackNames = part.tracks.map((track) => track.name).join(', ');
	const description = truncate(
		`${questionCount} free practice questions on ${part.title}, across ${part.tracks.length} tracks: ${trackNames}. Write Python and run the tests in your browser.`,
		160
	);

	return {
		title: withSiteName(`${part.title} practice questions`),
		description,
		path,
		jsonLd: [
			{
				'@context': 'https://schema.org',
				'@type': 'CollectionPage',
				name: part.title,
				description,
				url: absoluteUrl(path),
				inLanguage: 'en',
				isAccessibleForFree: true
			},
			buildBreadcrumbJsonLd([
				{ name: 'Home', path: '/' },
				{ name: 'Questions', path: '/questions' },
				{ name: part.title, path }
			])
		]
	};
}
